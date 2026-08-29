function StatCard({ title, value, subtitle, icon }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>

          <p className="text-3xl font-bold text-slate-800 mt-2">{value}</p>

          {subtitle && (
            <p className="text-xs text-slate-500 mt-2">{subtitle}</p>
          )}
        </div>

        <div className="text-2xl">{icon}</div>
      </div>
    </div>
  );
}

export default StatCard;
