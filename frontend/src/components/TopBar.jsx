import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import TextInput from "./TextInput";
import logo from "../assets/logo_v2.png";
import CustomButton from "./CustomButton";
import { useForm } from "react-hook-form";
import { BsMoon, BsSunFill } from "react-icons/bs";
import { IoMdNotificationsOutline } from "react-icons/io";
import { SetTheme } from "../Redux/theme";
import { logoutUser } from "../Redux/userSlice";

const TopBar = () => {
  const { theme } = useSelector((state) => state.theme);
  const { user } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleTheme = () => {
    const themeValue = theme === "light" ? "dark" : "light";

    dispatch(SetTheme(themeValue));
  };

  const handleSearch = async (data) => {};

  return (
    <div className="topbar w-full flex items-center justify-between rounded-lg py-2 px-4 bg-primary">
      <Link to="/" className="flex gap-2 items-center">
        <div className="flex gap-2 items-center">
          <img
            src={logo}
            alt=""
            width="60px"
            className="logo mt-2 ml-4 max-sm:ml-2"
          />
        </div>
      </Link>

      <form
        className="hidden md:flex items-center justify-center"
        onSubmit={handleSubmit(handleSearch)}
      >
        <TextInput
          placeholder="Search..."
          styles="w-[16rem] lg:w-[32rem] rounded-l-full py-2"
          register={register("search")}
        />
        <CustomButton
          title="Search"
          type="submit"
          containerStyles="bg-[#db4b4b] text-white px-4 py-2 rounded-r-full"
        />
      </form>

      {/* ICONS */}
      <div className="flex gap-3 items-center text-ascent-1 text-md md:text-lg">
        <button onClick={() => handleTheme()}>
          {theme == "dark" ? <BsMoon /> : <BsSunFill />}
        </button>
        <div className="hidden lg:flex">
          <IoMdNotificationsOutline />
        </div>

        <div>
          <Link to={"/login"}>
            <CustomButton
              onClick={() => dispatch(logoutUser())}
              title="Log Out"
              containerStyles="text-sm text-ascent-1 px-3 md:px-4 py-1 border border-[#666] rounded-full"
            />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
