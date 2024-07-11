import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useForm } from "react-hook-form";
import logo from "../assets/logo_v2.png";
import { BsShare } from "react-icons/bs";
import { ImConnection } from "react-icons/im";
import { AiOutlineInteraction } from "react-icons/ai";
import { TextInput, Loading, CustomButton } from "../components";
import bgImg from "../assets/img.png";
import { client } from "../client";
import { getUser } from "../Redux/userSlice";

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    mode: "onChange",
  });
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const onSubmit = async (data) => {
    try {
      await client.post('/api/login', {
        "username": data.username,
        "password": data.password
      });
      await dispatch(getUser());
      const from = location.state?.from?.pathname || '/';
      navigate(from, { replace: true });
    } catch (error) {
      console.log(error);
    }
  };

  const [errMsg, setErrMsg] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  return (
    <div className="bg-bgColor w-full h-[100vh] flex items-center justify-center p-6">
      <div className="w-full md:w-2/3 h-fit lg:h-full 2xl:h-5/6 py-8 lg:py-0 flex bg-primary rounded-xl overflow-hidden shadow-xl">
        {/* Left section */}
        <div className="w-full lg:w-1/2 h-full p-10 2xl:px-20 flex flex-col justify-center">
          {/* LOGO  */}
          <div className="w-full flex gap-2 items-center mb-6">
            <img src={logo} alt="" className="logo" />
          </div>

          <p className="text-ascent-1 text-base font-semibold">
            Log in to your Account
          </p>
          <span className="text-sm mt-2 text-ascent-2">Welcome Back</span>
          <form className="py-8 flex flex-col gap-5" onSubmit={handleSubmit(onSubmit)}>
            <TextInput
              name="username"
              placeholder="Username"
              label="username"
              type="text"
              register={register("username", {
                required: "Username is required",
              })}
              styles="w-full rounded-full"
              labelStyle="ml-2"
              error={errors.username ? errors.username.message : ""}
            />

            <TextInput
              name="password"
              placeholder="Password"
              label="Password"
              type="password"
              labelStyle="ml-2"
              register={register("password", {
                required: " Password is required!",
              })}
              styles="w-full rounded-full"
              error={errors.password ? errors.password?.message : ""}
            />
            <Link
              to="/reset-password"
              className="text-right font-semibold text-red text-sm "
            >
              Forgot Password ?
            </Link>

            {errMsg?.message && (
              <span
                className={`text-sm ${
                  errMsg?.status == "failed"
                    ? "text-[#f64949fe"
                    : "text-[#2ba150fe]"
                } mt-0.5 `}
              >
                {errMsg?.message}
              </span>
            )}

            {isSubmitting ? (
              <Loading />
            ) : (
              <CustomButton
                type="submit"
                containerStyles={`inline-flex justify-center rounded-md bg-red px-8 py-3 text-sm font-medium text-white outline-none`}
                title="Login"
              />
            )}
          </form>

          <p className="text-ascent-2 text-sm text-center">
            Don't have an account?
            <Link
              to="/register"
              className="text-[#db4b4b] font-semibold ml-2 cursor-pointer"
            >
              Create Account
            </Link>
          </p>
        </div>
        {/* right */}
        <div className=" w-1/2 h-full lg:flex flex-col items-center justify-center bg-red">
          <div className="relative w-full flex items-center justify-center">
            <img
              src={bgImg}
              alt="bg Image"
              className="w-48 2xl:w-64 h-48 2xl:h-64 rounded-full object-cover"
            />
            {/*Icons next to images*/}
            <div className="absolute flex items-center gap-1 bg-white right-10 top-10 py-2 px-5 rounded-full">
              <BsShare size={14} />
              <span className="text-xs font-medium">Share</span>
            </div>

            <div className="absolute flex items-center gap-1 bg-white left-8 top-6 py-2 px-5 rounded-full">
              <ImConnection />
              <span className="text-xs font-medium">Connect</span>
            </div>

            <div className="absolute flex items-center gap-1 bg-white left-10 bottom-6 py-2 px-5 rounded-full">
              <AiOutlineInteraction />
              <span className="text-xs font-medium">Interact</span>
            </div>
          </div>

          <div className="mt-16 text-center">
            <p className="text-white text-base">
              Connect with friends & have share for fun
            </p>
            <span className="text-sm text-white/80">
              Share knowledge with students and the world.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
