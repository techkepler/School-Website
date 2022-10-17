import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../contexts/GlobalProvider";
import { SchoolBgImg1 } from "../../../Assets/export/ExportImg";
import axiosPublic from "../../../Api/axiosPublic";

const LogIn = () => {
  const navigate = useNavigate();
  const { setAuth, setCurrentLocation } = useAuth();
  const initalValue = {
    uid: "",
    password: "",
  };

  useEffect(() => {
    setCurrentLocation("Login");
  }, [setCurrentLocation]);

  const [trust, setTrust] = useState(false);

  const [data, setData] = useState(initalValue);
  const [status, setStatus] = useState({
    msg: "",
  });

  const [errorMsg, setErrorMsg] = useState({
    msg: "",
  });

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    localStorage.setItem("trust", trust);
    try {
      const response = await axiosPublic.post(
        "users/login/",
        {
          uid: data.uid,
          password: data.password,
        },
        { withCredentials: true }
      );
      setStatus({ msg: response.data.msg });
      setAuth({
        token: response.data.token,
        role: response.data.role,
        name: response.data.name,
        uid: response.data.uid,
        category: response.data.category,
        email: response.data.email,
        grade: response.data.grade,
      });
      setTimeout(() => {
        if (response.data.role[1] === 2481237951) {
          navigate("/student/");
        } else if (response.data.role[1] === 5379482180) {
          navigate("/staff/");
        } else if (response.data.role[1] === 2846728426) {
          navigate("/admin/");
        }
      }, 1000);
    } catch (error) {
      if (!error?.response) {
        setErrorMsg({ msg: "No repsonse from server." });
        setTimeout(() => {
          setErrorMsg({ msg: null });
        }, 3000);
      } else if (error.response?.status === 401) {
        setErrorMsg({ msg: "UnAuthorized" });
        setTimeout(() => {
          setErrorMsg({ msg: null });
        }, 3000);
      } else if (error.response?.status === 500) {
        setErrorMsg({ msg: "Internal Sever Error" });
        setTimeout(() => {
          setErrorMsg({ msg: null });
        }, 3000);
      } else {
        setErrorMsg({ msg: error.response.data.msg });
        setTimeout(() => {
          setErrorMsg({ msg: null });
        }, 3000);
      }
    }
  };

  const handleTrustChange = () => {
    setTrust((prev) => !prev);
  };

  return (
    <section
      className="overflow-y-auto h-[100vh] relative"
      style={{ backgroundImage: `url(${SchoolBgImg1})` }}
    >
      {status.msg && (
        <div className="items-center w-full relative  flex justify-center">
          <p className="px-4 lg:px-24 text-base  top-2  py-2  text-gray-900 bg-green-500 mx-2 rounded-md fixed z-10 text-center">
            {status.msg}
          </p>
        </div>
      )}

      {errorMsg.msg && (
        <div className="items-center w-full relative  flex   justify-center ">
          <p className="px-4 lg:px-14 text-base top-2 capitalize py-2  text-gray-900 bg-red-500 rounded-md fixed text-center z-10">
            {errorMsg.msg}
          </p>
        </div>
      )}

      <div className="flex flex-col justify-center items-center px-2">
        <div className="usr-passowrd lg:absolute mt-5 w-full sm:w-80 lg:w-72  bg-[#004b87] text-white rounded-lg right-2 top-2 px-6 py-6">
          <h1 className="text-center font-semibold text-lg mb-4">
            Users Credentials
          </h1>
          <div className="admin-user-credentials mb-3">
            <h2 className="font-semibold ">For Admin Section:</h2>
            <p className="text-sm">
              User ID: <span>admin</span>{" "}
            </p>
            <p className="text-sm">
              Password: <span>Admin@123</span>{" "}
            </p>
          </div>
          <div className="teacher-user-credentials my-3">
            <h2 className="font-semibold ">For Teacher Section:</h2>
            <p className=" text-sm">
              User ID: <span>IS835KSER</span>{" "}
            </p>
            <p className="text-sm">
              Password: <span>Teacher@123</span>{" "}
            </p>
          </div>
          <div className="student-user-credentials my-3">
            <h2 className="font-semibold ">For Student Section</h2>
            <p className="text-sm">
              User ID: <span>SKE83KSTK</span>{" "}
            </p>
            <p className="text-sm">
              Password: <span>Student@123</span>{" "}
            </p>
          </div>
        </div>
        <div className="my-24 bg-[#004b87] w-full sm:w-[28rem] py-8 px-6 rounded-lg md:px-8 ">
          <h1 className="text-3xl text-gray-300 text-center">Sign In</h1>
          <form onSubmit={handleSubmit} className="mt-8">
            <div className="usr-uid relative group my-8">
              <label
                htmlFor="uid"
                className=" left-4 px-1 my-1 block text-lg  text-white"
              >
                User Id
              </label>
              <input
                type="uid"
                name="uid"
                id="uid"
                className="w-full py-4  group rounded-md  text-gray-800 px-2"
                onChange={handleChange}
              />
            </div>

            <div className="usr-password relative group my-8">
              <label
                htmlFor="password"
                className="px-1 block text-lg text-white my-1"
              >
                Password
              </label>
              <input
                type="password"
                name="password"
                id="password"
                className="w-full py-4  group rounded-md  px-2"
                onChange={handleChange}
              />
            </div>

            <div className="mt-14">
              <button
                className="bg-[#7582eb] w-full rounded-md py-4 text-sm font-semibold hover:bg-[#4453c8] text-black"
                disabled={data.uid.length < 1 || data.password.length < 1}
              >
                Login
              </button>

              <div className="trust-devic my-3 w-full">
                <input
                  type="checkbox"
                  id="checkbox"
                  className="form-checkbox"
                  onChange={handleTrustChange}
                  value={Boolean(trust)}
                />
                <label
                  htmlFor="checkbox"
                  className="text-gray-300 font-bold text-xs inline-block ml-2"
                >
                  Keep me logged in.
                  <span className="text-xs font-normal ml-1">
                    (Uncheck in share device.)
                  </span>
                </label>
              </div>
              {/* <div className="flex mt-5 justify-between items-center">
                <NavLink
                  to="/reset/password/uid/submit/"
                  className="text-sm  text-gray-300 block hover:underline hover:text-blue-500"
                >
                  Forgot Password?
                </NavLink>

                <NavLink
                  to="/register/"
                  className="text-sm  text-gray-300  block hover:underline hover:text-blue-500"
                >
                  Not registered yet?
                </NavLink>
              </div> */}
            </div>
          </form>
        </div>
      </div>
    </section>
  );
};

export default LogIn;
