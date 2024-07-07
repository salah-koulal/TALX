import {Outlet, Navigate, Route, Routes, useLocation } from "react-router-dom";
import {useSelector} from "react-redux"
import { Home, Login, Profile, Register, ResetPassword } from "./pages";
import { user } from "./assets/data.js";

function Layout(){
  const {user} = useSelector(state => state.user) ;
  const location = useLocation();
  // console.log({user}); 
  return user?.token?(
    <Outlet/>
  ): (
    <Navigate to='/home' state= {{from: location}} replace/>
  );
}
function App() {
  const { theme } = useSelector((state) => state.theme);
  console.log(theme);
  return (
    <div data-theme={theme} className="w-full min-h-[100vh]">
      <Routes>
        <Route element={<Layout />}></Route>
        <Route path="/" element={<Home />} />
        <Route path="/profile/:id?" element={<Profile />} />

        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />
      </Routes>
    </div>
  );
}


export default App;