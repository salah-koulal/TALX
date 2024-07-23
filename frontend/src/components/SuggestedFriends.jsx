import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { NoProfile } from "../assets/idx.js";
import { useSelector, useDispatch } from "react-redux";
import { getFollowers, getFollowing } from "../Redux/userSlice.js";
import { client } from "../client.js";
import { BsFiletypeGif, BsPersonFillAdd, BsPersonFill } from "react-icons/bs";

const SuggestedFriends = () => {
  const { user } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [suggestedFriends, setSuggestedFriends] = useState(null);
  const [followed, setFollowed] = useState(false);
  console.log("friend sug", suggestedFriends);
  const getProfiles = async () => {
    const data = await client.get('/api/profiles');
    const profiles = await data.data;
    console.log("profiles", profiles);
    const suggestedProfiles = profiles.filter(profile => profile.id !== user.id).slice(0, 5);
    setSuggestedFriends(suggestedProfiles);
  }

  const handleFollow = async (friend) => {
    const resp = await client.post(`/api/users/${friend.user.username}/follow/`);
    console.log("resp follow", resp.data)
    dispatch(getFollowing(user?.user?.username));
    setFollowed(prev => !prev)
    return resp.data;
  };

  useEffect(() =>{
    if (user)
      getProfiles();
  }, []);
  return (
    <div>
      <div className="w-full bg-primary shadow-inner shadow-[#94949457]   rounded-lg px-5 py-5">
            <div className="flex items-center justify-between text-lg text-ascent-1 border-b border-[#66666645]">
              <span>Friend Suggestion</span>
            </div>
            <div className="w-full flex flex-col gap-4 pt-4">
              {suggestedFriends?.map((friend) => (
                <div
                  className="flex items-center justify-between"
                  key={friend.id}
                >
                  <Link
                    to={"/profile/" + friend?.user?.username}
                    key={friend?.id}
                    className="w-full flex gap-4 items-center cursor-pointer"
                  >
                    <img
                      src={friend?.profileimg ?? NoProfile}
                      alt={friend?.first_name}
                      className="w-10 h-10 object-cover rounded-full"
                    />
                    <div className="flex-1 ">
                      <p className="text-base font-medium text-ascent-1">
                        {friend?.user?.first_name} {friend?.user?.last_name}
                      </p>
                      <span className="text-sm text-ascent-2">
                      {(friend?.profession && friend?.profession !== '') ? friend?.profession : "No Profession"}
                      </span>
                    </div>
                  </Link>

                  <div className="flex gap-1">
                    <button
                      className="bg-[#0459a430] text-sm text-white p-1 rounded"
                      onClick={() => {handleFollow(friend)}}
                    >
                      <BsPersonFillAdd size={20} className="text-[#0095f6]" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
    </div>
  );
};

export default SuggestedFriends;
