import {Outlet, Navigate, Route, Routes, useLocation } from "react-router-dom";
import {useSelector, useDispatch} from "react-redux"
import { Home, Login, Profile, Register, ResetPassword } from "./pages";
import { Loading } from "./components";
import { getUser } from "./Redux/userSlice.js";
import { user } from "./assets/data.js";
import { useEffect } from 'react'

function Layout(){
  const { user, status } = useSelector(state => state.user);
  const dispatch = useDispatch();
  const location = useLocation();
  useEffect(() => {
    if (status === 'idle') dispatch(getUser());
  }, [dispatch, status])
  console.log("Layout: User state", user);
  console.log("Layout: Status", status);
  if (status === "loading") return <Loading />;
  return status === 'failed'?(
    <Navigate to='/login' state= {{from: location}} replace/>
  ): (
    <Outlet/>
  );
}
function App() {
  const { theme } = useSelector((state) => state.theme);
  console.log(theme);
  return (
    <div data-theme={theme} className="w-full min-h-[100vh]">
      <Routes>
        {/* Protected Routes */}
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/profile/:username?" element={<Profile />} />
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