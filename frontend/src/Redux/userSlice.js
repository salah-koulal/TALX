import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { client } from "../client";
//import { user } from "../assets/data";

export const getUser = createAsyncThunk('user/getUser', async () => {
  const user = await client.get('/api/user', { withCredentials: true });
  const profile = await client.get(`/api/profiles/${user.data.user.username}`);
  return profile.data
});

export const logoutUser = createAsyncThunk('user/logout', async () => {
  await client.post('/api/logout', { withCredintials: true });
});

/*const getProfile = async (username) => {
  const profile = await client.get(`/api/profiles/${username}`);
  return profile.data
};*/

export const getFollowers = createAsyncThunk('user/getFollowers', async (username) => {
  const users = await client.get(`/api/users/${username}/followers`);
  return users.data;
  /*const data = await users.data;
  const profiles = data.map(async user => await getProfile(user.username));
  return profiles*/
});

export const getFollowing = createAsyncThunk('user/getFollowing', async (username) => {
  const users = await client.get(`/api/users/${username}/following`);
  return users.data
  /*const data = await users.data;
  const profiles = data.map(async user => await getProfile(user.username));
  return profiles*/
});

const initialState = {
  user: null,
  status: 'idle',
  error: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  extraReducers: (builder) => {
    builder
      .addCase(getUser.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(getUser.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.user = action.payload;
      })
      .addCase(getUser.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(logoutUser.fulfilled, (state) => {
        state.user = null;
        state.status = 'idle';
      })
      .addCase(getFollowers.fulfilled, (state, action) => {
        if (JSON.stringify(state.followers) !== JSON.stringify(action.payload)) {
          state.followers = action.payload;
        }
      })
      .addCase(getFollowing.fulfilled, (state, action) => {
        if (JSON.stringify(state.following) !== JSON.stringify(action.payload)) {
          state.following = action.payload;
        }
      })
  }
});


export default userSlice.reducer;
/*const initialState = {
  user: JSON.parse(window?.localStorage.getItem("user")) ?? user,
  edit: false,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    login(state, action) {
      state.user = action.payload;
      localStorage.setItem("user", JSON.stringify(action.payload));
    },
    logout(state) {
      state.user = null;
      localStorage?.removeItem("user");
    },
    updateProfile(state, action) {
      state.edit = action.payload;
    },
  },
});
export default userSlice.reducer;


export function UserLogin(user) {
  return (dispatch, getState) => {
    dispatch(userSlice.actions.login(user));
  };
}
*/
/*export function Logout() {
  return (dispatch, getState) => {
    dispatch(logoutUser());
  };
}*/
export function UpdateProfile(val) {
  return (dispatch, getState) => {
    dispatch(userSlice.actions.updateProfile(val));
  };
}
