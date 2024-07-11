import { Outlet, Navigate, Route, Routes, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import { Home, Login, Profile, Register, ResetPassword } from "./pages";

function Layout() {
  const { user } = useSelector((state) => state.user);
  const location = useLocation();
<<<<<<< HEAD

  return user?.token ? (
    <Outlet />
  ) : (
    <Navigate to="/login" state={{ from: location }} replace />
=======
  console.log("Layout: User state", user); 
  return user?(
    <Outlet/>
  ): (
    <Navigate to='/login' state= {{from: location}} replace/>
>>>>>>> 73b653b3b6bb1a6dc86f376576f49ede2f5168ec
  );
}

function App() {
  const { theme } = useSelector((state) => state.theme);

  return (
    <div data-theme={theme} className="w-full min-h-[100vh]">
      <Routes>
<<<<<<< HEAD
=======
        {/* Protected Routes */}
>>>>>>> 73b653b3b6bb1a6dc86f376576f49ede2f5168ec
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/profile/:id?" element={<Profile />} />
        </Route>

        {/* Public Routes */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />
      </Routes>
    </div>
  );
}

export default App;
