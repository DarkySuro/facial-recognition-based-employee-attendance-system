import { NavLink } from "react-router-dom";

const navItems = [
  {
    name: "Dashboard",
    path: "/",
    icon: "📊",
  },
  {
    name: "Employees",
    path: "/employees",
    icon: "👥",
  },
  {
    name: "Enrollment",
    path: "/enrollment",
    icon: "📷",
  },
  {
    name: "Attendance",
    path: "/attendance",
    icon: "✓",
  },
  {
    name: "Recognition Log",
    path: "/recognition-log",
    icon: "👁",
  },
];

function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen p-5 flex flex-col">
      <div className="mb-10">
        <h1 className="text-xl font-bold">🛡️ Attendance AI</h1>

        <p className="text-sm text-slate-400 mt-1">Face Recognition System</p>
      </div>

      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `
              flex items-center gap-3
              px-4 py-3
              rounded-lg
              transition
              ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }
              `
            }
          >
            <span>{item.icon}</span>

            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto text-xs text-slate-500">Presentation MVP</div>
    </aside>
  );
}

export default Sidebar;
