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
import { client } from "../client.js";


const Profile = () => {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [follows, setFollows] = useState(null);
  const { user } = useSelector((state) => state.user);
  const [edit, setEdit] = useState(false);
  const dispatch = useDispatch();
  const { following } = useSelector((state) => state.user);

  const getProfile = async (username) => {
    const profile = await client.get(`/api/profiles/${username}`);
    const data = await profile.data;
    setProfile(data);
  }
  const getFollows = async (username) => {
    const profile = await client.get(`/api/users/${username}/following`);
    const data = await profile.data;
    setFollows(data);
  }
  useEffect(()=> {
    if (username) {
      getProfile(username);
      getFollows(username);
    } else {
      setProfile(user);
      setFollows(following);
    }
  }, []);
  return (
    <div className="w-full h-screen flex justify-center items-center bg-secondary">
      <div className="lg:w-1/3 md:w-1/2 w-full max-w-md bg-primary flex flex-col items-center  shadow-inner shadow-[#94949457]  rounded-xl px-6 py-4 ">
        <div className="w-full flex items-center justify-between border-b pb-5 border-[#66666645]">
          <Link to={"/profile/" + profile?.user?.username} className="flex gap-2">
            <img
              src={profile?.profileimg ?? NoProfile}
              alt={profile?.user?.email}
              className="w-14 h-14 object-cover rounded-full"
            />

            <div className="flex flex-col justify-center">
              <p className="text-lg font-medium text-ascent-1">
                {profile?.user?.first_name} {profile?.user?.last_name}
              </p>
              <p className="text-lg font-medium text-ascent-2">
                @{profile?.user?.username}
              </p>
            </div>
          </Link>
          {/* Update Profile if it is user */}
          <div className="">
            {profile?.id === user?.id ? (
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
            <span>{(profile?.location && profile?.profession !== '') ? profile?.location : "Add Location"}</span>
          </div>

          <div className="flex gap-2 items-center text-ascent-2">
            <BsBriefcase className=" text-lg text-ascent-1" />
            <span>{(profile?.profession && profile?.profession !== '') ? profile?.profession : "Add Profession"}</span>
          </div>
        </div>

        <div className="w-full flex flex-col gap-2 py-4 border-b border-[#66666645]">
          <h1 className="text-xl text-ascent-1 font-semibold">Bio</h1>
          <p className="text-ascent-2">{profile?.bio}</p>
        </div>

        <div className="w-full flex flex-col gap-2 py-4 border-b border-[#66666645]">
          <p className="text-xl text-ascent-1 font-semibold">
            {follows?.length} Friends
          </p>

          <div className="flex items-center justify-between">
            <span className="text-ascent-2">Who viewed your profile</span>
            <span className="text-ascent-1 text-lg">{/*user?.views?.length*/}1 views</span>
          </div>

          <span className="text-base text-[#0095f6]">
            {profile?.verified ? "Verified Account" : "Not Verified"}
          </span>

          <div className="flex items-center justify-between">
            <span className="text-ascent-2">Joined</span>
            <span className="text-ascent-1 text-base">
              {moment(profile?.created_at).fromNow()}
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

