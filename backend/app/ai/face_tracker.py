from dataclasses import dataclass
import math

import numpy as np


@dataclass
class FaceTrack:
    track_id: int
    bbox: np.ndarray
    missed_frames: int = 0


class FaceTracker:

    def __init__(
        self,
        max_distance: float = 100.0,
        max_missed_frames: int = 10,
    ):
        self.max_distance = max_distance
        self.max_missed_frames = max_missed_frames

        self.next_track_id = 1
        self.tracks: list[FaceTrack] = []

    @staticmethod
    def _center(
        bbox: np.ndarray,
    ) -> tuple[float, float]:

        x1, y1, x2, y2 = bbox

        return (
            (x1 + x2) / 2,
            (y1 + y2) / 2,
        )

    @staticmethod
    def _distance(
        point_a: tuple[float, float],
        point_b: tuple[float, float],
    ) -> float:

        return math.sqrt(
            (point_a[0] - point_b[0]) ** 2
            + (point_a[1] - point_b[1]) ** 2
        )

    def update(
        self,
        faces,
    ) -> list[tuple[int, object]]:

        detections = []

        for face in faces:

            bbox = face.bbox.astype(
                np.float32
            )

            detections.append(
                (bbox, face)
            )

        # No faces detected
        if not detections:

            for track in self.tracks:
                track.missed_frames += 1

            self._remove_expired_tracks()

            return []

        # No existing tracks
        if not self.tracks:

            results = []

            for bbox, face in detections:

                track = self._create_track(
                    bbox
                )

                results.append(
                    (track.track_id, face)
                )

            return results

        results = []

        matched_tracks = set()
        matched_detections = set()

        # -----------------------------------------
        # Calculate candidate matches
        # -----------------------------------------

        candidates = []

        for detection_index, (
            bbox,
            face,
        ) in enumerate(detections):

            detection_center = self._center(
                bbox
            )

            for track_index, track in enumerate(
                self.tracks
            ):

                if track_index in matched_tracks:
                    continue

                track_center = self._center(
                    track.bbox
                )

                distance = self._distance(
                    detection_center,
                    track_center,
                )

                if distance <= self.max_distance:

                    candidates.append(
                        (
                            distance,
                            track_index,
                            detection_index,
                        )
                    )

        # Closest matches first
        candidates.sort(
            key=lambda item: item[0]
        )

        # -----------------------------------------
        # Match detections to existing tracks
        # -----------------------------------------

        for (
            distance,
            track_index,
            detection_index,
        ) in candidates:

            if track_index in matched_tracks:
                continue

            if detection_index in matched_detections:
                continue

            track = self.tracks[
                track_index
            ]

            bbox, face = detections[
                detection_index
            ]

            track.bbox = bbox
            track.missed_frames = 0

            matched_tracks.add(
                track_index
            )

            matched_detections.add(
                detection_index
            )

            results.append(
                (
                    track.track_id,
                    face,
                )
            )

        # -----------------------------------------
        # Create tracks for new faces
        # -----------------------------------------

        for detection_index, (
            bbox,
            face,
        ) in enumerate(detections):

            if detection_index in matched_detections:
                continue

            track = self._create_track(
                bbox
            )

            results.append(
                (
                    track.track_id,
                    face,
                )
            )

        # -----------------------------------------
        # Mark unmatched tracks
        # -----------------------------------------

        for track_index, track in enumerate(
            self.tracks
        ):

            if track_index not in matched_tracks:

                track.missed_frames += 1

        self._remove_expired_tracks()

        return results

    def _create_track(
        self,
        bbox: np.ndarray,
    ) -> FaceTrack:

        track = FaceTrack(
            track_id=self.next_track_id,
            bbox=bbox,
        )

        self.next_track_id += 1

        self.tracks.append(
            track
        )

        return track

    def _remove_expired_tracks(
        self,
    ) -> None:

        self.tracks = [
            track
            for track in self.tracks
            if track.missed_frames
            <= self.max_missed_frames
        ]

    def reset(self) -> None:

        self.tracks.clear()

        self.next_track_id = 1