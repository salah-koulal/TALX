import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { NoProfile } from "../assets/idx.js";
import { useSelector, useDispatch } from "react-redux";
import { getFollowers } from "../Redux/userSlice.js";
import { client } from "../client.js";
import { BsFiletypeGif, BsPersonFillAdd } from "react-icons/bs";

const SuggestedFriends = () => {
  const { user } = useSelector((state) => state.user)
  const [suggestedFriends, setSuggestedFriends] = useState(null);
  console.log("friend sug", suggestedFriends);
  const getProfiles = async () => {
    const profiles = await client.get('/api/profiles');
    const suggestedProfiles = profiles.data.filter(profile => profile.id !== user.id).slice(0, 5);
    setSuggestedFriends(suggestedProfiles);
  }

  const handleFollow = async () => {
    const resp = await client.post(`/api/users/${user.user.username}/follow`);
    console.log("resp follow", resp.data)
    return resp.data;
  };

  useEffect(() =>{
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
                      onClick={handleFollow}
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
