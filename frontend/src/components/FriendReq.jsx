import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { NoProfile } from "../assets/idx.js";
import { useSelector, useDispatch } from "react-redux";
import { getFollowers } from "../Redux/userSlice.js";
import { client } from "../client.js";
import CustomButton from "./CustomButton.jsx";

const FriendReq = () => {
  const { user } = useSelector((state) => state.user);
  const { followers } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [friendRequest, setFriendRequest] = useState(null);
  console.log("friend req", friendRequest)
  useEffect(() =>{
    if (user?.user?.username && !followers) {
      dispatch(getFollowers(user?.user?.username));
    }
  }, [dispatch, user, followers]);
  useEffect(() => {
    if (followers) {
      Promise.all(followers.map(user => client.get(`/api/profiles/${user.username}`)))
        .then(responses => responses.map(res => res.data))
        .then(profiles => setFriendRequest(profiles));
    }
  }, [followers]);
  return (
    <div>
      <div className="w-full bg-primary shadow-inner shadow-[#94949457]    rounded-lg px-6 py-5">
        <div className="flex items-center justify-between text-xl text-ascent-1 pb-2 border-b border-[#66666645]">
            <span>Friend Request</span>
            <span>{friendRequest?.length}</span>
        </div>
        <div className="w-full flex flex-col  gap-4 pt-4">
            {friendRequest?.map(({ friend }) => (
            <div key={friend?.id} className="flex items-center justify-between">
                <Link
                to={"/profile" + friend?.user?.username}
                className="w-full flex gap-4 items-center cursor-pointer"
                >
                    <img
                        src={friend?.profileimg ?? NoProfile}
                        alt={friend?.user?.first_name}
                        className="w-10 h-10 object-cover rounded-full"
                    />
                    <div className="flex-1">
                        <p className="text-base font-medium text-ascent-1">
                        {friend?.first_name} {friend?.last_name}
                        </p>
                        <span className="text-sm text-ascent-2">
                        {friend?.profession ?? "No Profession"}
                        </span>
                    </div>
                </Link>

                  <div className="flex gap-1">
                    <CustomButton
                      title="Accept"
                      containerStyles="bg-[#0095f6] text-xs text-white px-1.5 py-1 rounded-full"
                    />
                    <CustomButton
                      title="Deny"
                      containerStyles="border border-[#666] text-xs text-ascent-1 px-1.5 py-1 rounded-full"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
    </div>
  );
};

export default FriendReq;
