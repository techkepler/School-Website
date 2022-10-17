import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../../contexts/GlobalProvider";
import { DashBoardItems } from "../../Data/HomeAdmin";
import StudentChart from "../../../Admin/Chart/StudentChart";
import FeeCollectionChart from "../../../Admin/Chart/FeeCollectionChart";
import PerformanceChart from "../../../Admin/Chart/PerformanceChart";
import StuRatioChart from "../../../Admin/Chart/StuRatioChart";
import YearlyRevenueChart from "../../../Admin/Chart/YearlyRevenueChart";
import Footer from "../../../Admin/layouts/footer/Footer";
import "../css/Home.css";

const HomeStaff = () => {
  const { isSideBar, isColorBar, themeColor } = useAuth();
  return (
    <div
      className={` mt-2 px-4 md:px-6 lg:px-10  admin-body ${
        isSideBar && "sidebar-active"
      } ${isColorBar && "colorbar-active"}`}
    >
      <div>
        <h2
          className="text-center text-xl md:text-2xl font-semibold my-10 text-slate-700 dark:text-slate-300 antialiased"
          style={{ color: themeColor }}
        >
          Asgard Student Dashboard
        </h2>

        <div className="flex items-center justify-center flex-col">
          <div className="flex flex-wrap gap-3 md:gap-6 items-center justify-center  w-full md:w-[90%] lg:w-[80%] mb-10">
            {DashBoardItems().map((data, index) => (
              <Link
                to={`/student/${data.link}/`}
                className={`teacher flex flex-col gap-2 items-center justify-center  bg-slate-100 dark:bg-slate-700 py-4 rounded-md hover:bg-slate-200 dark:hover:bg-slate-600 cursor-pointer w-[48%] md:w-[30%] ${
                  isSideBar || isColorBar ? "h-28 md:h-24" : "h-28 md:h-32"
                }`}
                key={index}
              >
                {data.icon}
                <p
                  className="dark:text-slate-300 font-semibold text-xs capitalize"
                  style={{ color: themeColor }}
                >
                  {data.name}
                </p>
              </Link>
            ))}
          </div>

          <StudentChart />
          <FeeCollectionChart />
          <PerformanceChart />
          <YearlyRevenueChart />
          <StuRatioChart />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default HomeStaff;
