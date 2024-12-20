import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { NoProfile } from "../assets/idx.js";
import { useSelector } from "react-redux";
import {
  CustomButton,
  FriendsCard,
  Loading,
  ProfileCard,
  TextInput,
  TopBar,
  FriendReq,
  SuggestedFriends
} from "../components";
import { requests, friends, suggest, posts } from "../assets/data";
import { BsFiletypeGif, BsPersonFillAdd } from "react-icons/bs";
import { BiImages, BiSolidVideo } from "react-icons/bi";
import { useForm } from "react-hook-form";
import PostCard from "../components/PostCard.jsx";
import { selectAllPosts } from "../Redux/postSlice.js";
import { client } from "../client.js";
import { useDispatch } from "react-redux";
import { getUser, getFollowers, getFollowing } from "../Redux/userSlice.js"
import { getPosts, createPost } from "../Redux/postSlice.js";

const test = async () => {
  const user = await client.get('/api/user', { withCredentials: true });
  //console.log(user);
  const profile = await client.get(`/api/profiles/${user.data.user.username}`);
  return profile.data
}

const Home = () => {
  const { user } = useSelector((state) => state.user);
  //console.log(test());
  console.log("user", user);
  const posts = useSelector(selectAllPosts);
  const postStatus = useSelector(state => state.posts.status);
  console.log("posts", posts);
  const [friendRequest, setFriendRequest] = useState(requests);
  const [suggestedFriends, setSuggestedFriends] = useState(suggest);
  const [errMsg, setErrMsg] = useState("");
  const [file, setFile] = useState(null);
  const [posting, setPosting] = useState(false);
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    // dispatch(getUser());
    if (postStatus === "idle") {
      dispatch(getPosts());
    }
    dispatch(getFollowers(user?.user?.username));
    dispatch(getFollowing(user?.user?.username));
  }, [dispatch, postStatus, user])

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm();
  const handlePostSubmit = (data) => {
    /*await client.post('/api/posts', {
      content: data.description,
      type: 'meme',
      //Image
    });
    dispatch(getPosts())*/
    const formData = new FormData();
    formData.append('content', data.description);
    formData.append('type', 'meme');
    if (file) {
      formData.append('image', file);
    }
    dispatch(createPost(formData));
    reset()
  };
  return (
    <div className="w-full px-20 lg:px-10 pb-20 2xl:px-40 bg-bgColor  h-screen overflow-hidden">
      <TopBar />

      <div className="w-full flex gap-2 lg:gap-4 pt-5 pb-10 h-full">
        {/* LEFT */}
        <div className="hidden w-1/3 lg:w-1/4 h-full md:flex flex-col gap-6 overflow-y-auto">
          <ProfileCard />
          <FriendsCard />
        </div>

        {/* CENTER */}
        <div className="flex-1 h-full bg-primary px-4 flex flex-col gap-6 overflow-y-auto rounded-lg">
          <form
            onSubmit={handleSubmit(handlePostSubmit)}
            className="bg-primary px-4 rounded-lg"
          >
            <div className="w-full flex items-center gap-2 py-4 border-b border-[#66666645]">
              <img
                src={user?.profileimg ?? NoProfile}
                alt={user?.user?.email}
                className="w-14 h-14 object-cover rounded-full"
              />
              <TextInput
                styles="w-full rounded-full py-5"
                placeholder="What's on your mind...."
                name="description"
                register={register("description", {
                  required: "Write Something about the post",
                })}
                error={errors.description ? errors.description.message : ""}
              />
            </div>
            {errMsg?.message && (
              <span
                role="alert"
                className={`text-sm ${
                  errMsg?.status === "failed"
                    ? "text-[#f64949fe]"
                    : "text-[#2ba150fe]"
                } mt-0.5`}
              >
                {errMsg?.message}
              </span>
            )}

            {/* Labels for Post Img,Vid,Gifs  */}
            <div className="flex items-center justify-between py-4 ">
              {/* IMGUpload */}
              <label
                htmlFor="imgUpload"
                className="flex items-center gap-1 text-base text-ascent-2 hover:text-ascent-1 cursor-pointer"
              >
                <input
                  type="file"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                  id="imgUpload"
                  data-max-size="5120"
                  accept=".jpg, .png, .jpeg"
                />
                <BiImages />
                <span>Image</span>
              </label>

              {/* VidUpload */}
              <label
                className="flex items-center gap-1 text-base text-ascent-2 hover:text-ascent-1 cursor-pointer"
                htmlFor="videoUpload"
              >
                <input
                  type="file"
                  data-max-size="5120"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                  id="videoUpload"
                  accept=".mp4, .wav"
                />
                <BiSolidVideo />
                <span>Video</span>
              </label>

              {/* GifUpload */}
              <label
                className="flex items-center gap-1 text-base text-ascent-2 hover:text-ascent-1 cursor-pointer"
                htmlFor="gifUpload"
              >
                <input
                  type="file"
                  data-max-size="5120"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                  id="gifUpload"
                  accept=".gif"
                />
                <BsFiletypeGif />
                <span>Gif</span>
              </label>
              <div>
                {posting ? (
                  <Loading />
                ) : (
                  <CustomButton
                    type="submit"
                    title="Post"
                    containerStyles="bg-[#db4b4b] text-white py-1 px-6 rounded-full font-semibold text-sm"
                  />
                )}
              </div>
            </div>
          </form>
          {loading ? (
            <Loading />
          ) : posts?.length > 0 ? (
            posts?.map((post) => (
              <PostCard
                key={post?.id}
                post={post}
                /*user={user}
                deletePost={() => {}}
                likePost={() => {}}*/
              />
            ))
          ) : (
            <div className="flex w-full h-full items-center justify-center">
              <p className="text-lg text-ascent-2">No Post Available</p>
            </div>
          )}
        </div>

        {/* RIGHT */}
        <div className="hidden w-1/4 h-full lg:flex flex-col gap-8 overflow-y-auto">
          {/* Friend Req */}
          {/* <div className="w-full bg-primary shadow-inner shadow-[#94949457]    rounded-lg px-6 py-5">
            <div className="flex items-center justify-between text-xl text-ascent-1 pb-2 border-b border-[#66666645]">
              <span>Friend Request</span>
              <span>{friendRequest?.length}</span>
            </div>
            <div className="w-full flex flex-col  gap-4 pt-4">
              {friendRequest?.map(({ _id, requestFrom: from }) => (
                <div key={_id} className="flex items-center justify-between">
                  <Link
                    to={"/profile" + from._id}
                    className="w-full flex gap-4 items-center cursor-pointer"
                  >
                    <img
                      src={from?.profileUrl ?? NoProfile}
                      alt={from?.firstName}
                      className="w-10 h-10 object-cover rounded-full"
                    />
                    <div className="flex-1">
                      <p className="text-base font-medium text-ascent-1">
                        {from?.firstName} {from?.lastName}
                      </p>
                      <span className="text-sm text-ascent-2">
                        {from?.profession ?? "No Profession"}
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
          </div> */}
          <FriendReq />

          {/* Suggested Friends */}
          {/* <div className="w-full bg-primary shadow-inner shadow-[#94949457]   rounded-lg px-5 py-5">
            <div className="flex items-center justify-between text-lg text-ascent-1 border-b border-[#66666645]">
              <span>Friend Suggestion</span>
            </div>
            <div className="w-full flex flex-col gap-4 pt-4">
              {suggestedFriends?.map((friend) => (
                <div
                  className="flex items-center justify-between"
                  key={friend._id}
                >
                  <Link
                    to={"/profile/" + friend?._id}
                    key={friend?._id}
                    className="w-full flex gap-4 items-center cursor-pointer"
                  >
                    <img
                      src={friend?.profileUrl ?? NoProfile}
                      alt={friend?.firstName}
                      className="w-10 h-10 object-cover rounded-full"
                    />
                    <div className="flex-1 ">
                      <p className="text-base font-medium text-ascent-1">
                        {friend?.firstName} {friend?.lastName}
                      </p>
                      <span className="text-sm text-ascent-2">
                        {friend?.profession ?? "No Profession"}
                      </span>
                    </div>
                  </Link>

                  <div className="flex gap-1">
                    <button
                      className="bg-[#0459a430] text-sm text-white p-1 rounded"
                      onClick={() => {}}
                    >
                      <BsPersonFillAdd size={20} className="text-[#0095f6]" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div> */}
          <SuggestedFriends />

        </div>
      </div>
    </div>
  );
};

export default Home;
