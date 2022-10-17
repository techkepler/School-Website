import React from "react";

import StudentChart from "../../../../Chart/StudentChart";
import FeeCollectionChart from "../../../../Chart/FeeCollectionChart";
import StuRatioChart from "../../../../Chart/StuRatioChart";

import StafPdfBtn from "./pdfBtn";
import AdminNav from "../../../../layouts/navbar/AdminNav";
import Footer from "../../../../layouts/footer/Footer";
import { useAuth } from "../../../../../contexts/GlobalProvider";
import ColorSettings from "../../../../Components/nav/ColorSettings";

const StaffPdf = () => {
  const { isSideBar, isColorBar, themeColor } = useAuth();

  return (
    <>
      <AdminNav />
      <section
        className={`teachers mt-2 px-4 md:px-6 lg:px-10  admin-body ${
          isSideBar && "sidebar-active"
        } ${isColorBar && "colorbar-active"}`}
      >
        <h2
          className="text-center text-xl md:text-2xl font-semibold my-10 text-slate-700 dark:text-slate-300"
          style={{ color: themeColor }}
        >
          Asgard Generate Staff PDF
        </h2>
        <div className="flex items-center justify-center flex-col ">
          <div className="flex flex-wrap gap-3 md:gap-6 items-center justify-center md:w-[90%] lg:w-[80%] w-full mb-10">
            <StafPdfBtn />
          </div>

          <StudentChart title={"Staff"} />
          <FeeCollectionChart title={"Staff Payment Report"} />
          <StuRatioChart title={"Staff"} />
        </div>
      </section>
      <ColorSettings />
      <Footer />
    </>
  );
};

export default StaffPdf;
