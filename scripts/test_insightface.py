import insightface

def main():
    print("InsightFace import successful.")
    print(f"InsightFace version: {insightface.__version__}")

    print("Creating FaceAnalysis model...")

    app = insightface.app.FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"],
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640),
    )

    print("InsightFace model initialized successfully.")


if __name__ == "__main__":
    main()