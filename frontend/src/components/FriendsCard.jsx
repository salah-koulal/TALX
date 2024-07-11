import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { NoProfile } from "../assets/idx.js";
import { useSelector, useDispatch } from "react-redux";
import { getFollowing } from "../Redux/userSlice.js";
import { client } from "../client.js";

const FriendsCard = () => {
  const { user } = useSelector((state) => state.user);
  const { following } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [friends, setFriends] = useState(null);
  console.log(friends)
  useEffect(() =>{
    if (user?.user?.username && !following) {
      dispatch(getFollowing(user?.user?.username));
    }
  }, [dispatch, user, following]);
  useEffect(() => {
    if (following) {
      Promise.all(following.map(user => client.get(`/api/profiles/${user.username}`)))
        .then(responses => responses.map(res => res.data))
        .then(profiles => setFriends(profiles));
    }
  }, [following]);
  return (
    <div>
      <div className="w-full bg-primary shadow-inner shadow-[#94949457]   rounded-lg px-6 py-5">
        <div className="flex items-center justify-between text-ascent-1 pb-2 border-b border-[#66666645]">
          <span> Friends</span>
          <span>{friends?.length}</span>
        </div>

        <div className="w-full flex flex-col gap-4 pt-4">
          {friends?.map((friend) => (
            <Link
              to={"/profile/" + friend?.user?.username}
              key={friend?.id}
              className="w-full flex gap-4 items-center cursor-pointer"
            >
              <img
                src={friend?.profileimg ?? NoProfile}
                alt={friend?.user?.first_name}
                className="w-10 h-10 object-cover rounded-full"
              />
              <div className="flex-1">
                <p className="text-base font-medium text-ascent-1">
                  {friend?.user?.first_name} {friend?.user?.last_name}
                </p>
                <span className="text-sm text-ascent-2">
                {(friend?.profession && friend?.profession !== '') ? friend?.profession : "No Profession"}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FriendsCard;
