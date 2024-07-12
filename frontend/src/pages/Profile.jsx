import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { LiaEditSolid } from "react-icons/lia";
import { useParams } from "react-router-dom";
import {
  BsBriefcase,
  BsFacebook,
  BsInstagram,
  BsPersonFillAdd,
} from "react-icons/bs";
import { FaXTwitter } from "react-icons/fa6";
import { CiLocationOn } from "react-icons/ci";
import moment from "moment";
import { NoProfile } from "../assets/idx.js";
import { EditProfile } from "../components";
import { getUser, getFollowing } from "../Redux/userSlice";

const Profile = () => {
<<<<<<< HEAD
  return (
    <div>
      <h1>Profile</h1>
    </div>
  )
}
=======
  const { username } = useParams();
  console.log("usernameProfile", username);
  const { user } = useSelector((state) => state.user);
  const [edit, setEdit] = useState(false);
  const dispatch = useDispatch();
  const { following } = useSelector((state) => state.user);

  return (
    <div>
      <div className="w-full bg-primary flex flex-col items-center  shadow-inner shadow-[#94949457]  rounded-xl px-6 py-4 ">
        <div className="w-full flex items-center justify-between border-b pb-5 border-[#66666645]">
          <Link to={"/profile/" + user?.user?.username} className="flex gap-2">
            <img
              src={user?.profileimg ?? NoProfile}
              alt={user?.user?.email}
              className="w-14 h-14 object-cover rounded-full"
            />

            <div className="flex flex-col justify-center">
              <p className="text-lg font-medium text-ascent-1">
                {user?.user?.first_name} {user?.user?.last_name}
              </p>
              {/* <p className="text-lg font-medium text-ascent-2">
                @{user?.user?.username}
              </p> */}
              <span className="text-ascent-2">
                {(user?.profession && user?.profession !== '') ? user?.profession : "Add Profession"}
              </span>
            </div>
          </Link>
          {/* Update Profile if it is user */}
          <div className="">
            {user?.id ? (
              <LiaEditSolid
                size={22}
                className="text-red cursor-pointer "
                /*onClick={() => dispatch(UpdateProfile(true))}*/
                onClick={() => setEdit(true)}
              />
            ) : (
              <button
                className="bg-[#f9feff] text-sm text-white p-1 rounded"
                onClick={() => {}}
              >
                <BsPersonFillAdd size={20} className="text-[#f9667ae8]" />
              </button>
            )}
            {edit && <EditProfile close={() => {setEdit(false)}} />}
          </div>
        </div>
        {/* Brief Bio */}
        <div className="w-full flex flex-col gap-2 py-4 border-b border-[#66666645]">
          <div className="flex gap-2 items-center text-ascent-2">
            <CiLocationOn className="text-xl text-ascent-1" />
            <span>{(user?.location && user?.profession !== '') ? user?.location : "Add Location"}</span>
          </div>

          <div className="flex gap-2 items-center text-ascent-2">
            <BsBriefcase className=" text-lg text-ascent-1" />
            <span>{(user?.profession && user?.profession !== '') ? user?.profession : "Add Profession"}</span>
          </div>
        </div>
>>>>>>> 3a9ff5eb351486905d5d6119715edd836c77dc07

        <div className="w-full flex flex-col gap-2 py-4 border-b border-[#66666645]">
          <p className="text-xl text-ascent-1 font-semibold">
            {following?.length} Friends
          </p>

          <div className="flex items-center justify-between">
            <span className="text-ascent-2">Who viewed your profile</span>
            <span className="text-ascent-1 text-lg">{/*user?.views?.length*/}2 views</span>
          </div>

          <span className="text-base text-[#0095f6]">
            {user?.verified ? "Verified Account" : "Not Verified"}
          </span>

          <div className="flex items-center justify-between">
            <span className="text-ascent-2">Joined</span>
            <span className="text-ascent-1 text-base">
              {moment(user?.created_at).fromNow()}
            </span>
          </div>
        </div>
        {/* SoMed Links */}
        <div className="w-full gap-4 flex flex-col py-4 pb-6">
          <p className="text-ascent-1 text-lg font-semibold">Social Profile</p>
          <div className="flex gap-2 items-center text-ascent-2">
            <BsInstagram className=" text-xl text-ascent-1" />
            <span>Instagram</span>
          </div>
          <div className="flex gap-2 items-center text-ascent-2">
            <FaXTwitter className=" text-xl text-ascent-1" />
            <span>X</span>
          </div>
          <div className="flex gap-2 items-center text-ascent-2">
            <BsFacebook className=" text-xl text-ascent-1" />
            <span>Facebook</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;

