"use client";

import Image from "next/image";
import Dropdown from "./components/Dropdown";
import Marquee from "./components/Marquee";
import ProjectCard from "./components/ProjectCard";
import Carousel from "./components/Carousel";
import {
  LocationIcon,
  MailIcon,
  GlobeIcon,
  LinkedInIcon,
  GithubIcon,
  SpotifyIcon,
  Hamburger,
  XIcon,
} from "./svgs/Icons";
import { useState } from "react";
import './globals.css'

export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="pt-2 pb-8 lg:p-0 max-w-3xl mx-auto flex flex-col min-h-screen lg:flex lg:flex-row lg:gap-7 lg:justify-between lg:px-8 md:px-20 sm:px-24 px-4">
      <header
        className="lg:sticky lg:top-0 flex flex-col lg:max-h-screen md:flex md:flex-row lg:flex-col z-50 lg:w-[204px] lg:shrink-0 lg:gap-y-3 lg:py-10 md:gap-3 md:mx-0 
      mx-auto"
      >
        <div className="bg-white rounded-xl shadow-md p-2 flex sm:flex-row lg:flex-col lg:gap-3 relative">
          <img
            src="/static/ben_pfp22.png"
            className="h-auto w-32 lg:w-48 rounded-xl"
          />
          <div className="ml-2 pt-2 pr-2 lg:ml-1 lg:pt-0 lg:pr-0">
            <h1 className="text-gray-900 text-3xl lg:text-2xl font-medium lg:font-semibold tracking-tight leading-none">
              Hello I'm
            </h1>
            <h1 className="text-gray-900 text-3xl lg:text-2xl font-medium lg:font-semibold tracking-tight">
              Benjamin Garcia
            </h1>
            <h3 className="text-gray-700 text-base lg:text-lg leading-tight mt-2">
              I turn code into meaningful creations.
            </h3>
            <div className="flex flex-row gap-1 items-center mt-2">
              <LocationIcon />
              <p className="text-sm text-gray-500">Los Angeles, California</p>
            </div>
            <button
              onClick={toggleMenu}
              className="absolute top-2 right-2 block md:hidden lg:hidden"
            >
              {isMenuOpen ? <XIcon /> : <Hamburger />}
            </button>
          </div>
        </div>

        <div
          id="socials"
          className={`bg-white rounded-xl shadow-md p-2 flex flex-col gap-3 lg:p-3
              ${isMenuOpen ? "flex" : "hidden"} 
              top-full left-0 right-0 mt-2 z-50 flex flex-row justify-around items-center py-4 md:flex md:flex-col lg:flex lg:flex-col lg:mt-0 md:mt-0`}
        >
          <div className="flex flex-col gap-1">
            <a
              className="flex items-center gap-2 hover:underline text-sm md:-mt-2 md:mb-1 lg:mt-0 lg:mb-0"
              href="ben.com"
              target="_blank"
            >
              <GlobeIcon /> https://benjamin-garcia-v4.vercel.app/
            </a>
            <a
              className="flex items-center gap-2 hover:underline text-sm"
              href="mailto:bentgarcia05@gmail.com"
              target="_blank"
            >
              <MailIcon /> bentgarcia05@gmail.com
            </a>
          </div>
          <div className = "items-center flex flex-col md:-mt-6 lg:mt-0">
            <div className="flex flex-row items-center justify-center gap-6 mb-2">
              <a href="https://www.linkedin.com/in/btgarcia05/" target="_blank">
                <LinkedInIcon />
              </a>
              <a href="https://github.com/bgar324" target="_blank">
                <GithubIcon />
              </a>
              <a
                href="https://open.spotify.com/user/13loawolnhae7wiuu1ficd51g"
                target="_blank"
              >
                <SpotifyIcon />
              </a>
            </div>
            <a
              className="bg-black text-white rounded-xl px-4 py-1 text-sm w-fit mx-auto items-center justify-center hover:bg-black/90 font-semibold duration-300 transition ease-in-out"
              href="/static/resume.pdf"
              target="_blank"
            >
              Download My CV
            </a>
          </div>
        </div>
      </header>

      {/* <div className="flex flex-wrap gap-2 bg-white rounded-md shadow-md p-2 mt-4 text-xs">
        <a className="uppercase border px-2 py-1 rounded-lg">about</a>
        <a className="uppercase border px-2 py-1 rounded-lg">experience</a>
        <a className="uppercase border px-2 py-1 rounded-lg">tech stack</a>
        <a className="uppercase border px-2 py-1 rounded-lg">projects</a>
        <a className="uppercase border px-2 py-1 rounded-lg">education</a>
      </div> */}

      <main className="flex-1 flex-col lg:w-2/3 lg:py-13">
        <section id="about" className="flex flex-col">
          <p className="w-fit border border-gray-300 rounded-md px-2 py-1 lg:py-[.5px] text-xs lg:text-sm uppercase mt-10 lg:mt-0 lg:mb-5 font-semibold tracking-wider">
            about
          </p>
          <p className="text-gray-600 lg:text-lg leading-snug mt-4">
            I'm Benjamin Garcia, a second-year Computer Science major at Mt. San
            Antonio College, preparing to transfer to a four-year institution
            this fall. I’m a Web Developer focused on speed, responsiveness, and
            clean design.
          </p>
          <p className="mt-2 text-gray-600 lg:text-lg leading-snug ">
            Currently a Backend Software Developer Intern at TODD, I build fast,
            scalable websites that bridge design and functionality.
          </p>
        </section>

        <section id="experience" className="flex flex-col">
          <p className="w-fit border border-gray-300 rounded-md px-2 py-1 text-xs uppercase mt-10 mb-5 font-semibold tracking-wider lg:py-[.5px] lg:text-sm">
            experience
          </p>
          <div className="flex flex-col gap-4">
            <Dropdown
              role="Backend Software Development Intern"
              position="TODD"
              startDate="Apr 2025"
              endDate="Present"
              src="/static/companies/todd.jfif"
              description="Developing backend solutions that leverage AI and machine learning to automate large-scale agricultural data analysis and optimization."
            />
            <Dropdown
              role="Front-End Developer"
              position="Mt. SAC CS Club"
              startDate="Sep 2024"
              endDate="Present"
              src="/static/companies/mtsaccs.png"
              description="Redesigned and rebuilt the Mt. SAC CS Club website using React and Bootstrap, enhancing UX, responsiveness, and access to events, officers, and contact info for 900+ members."
            />
            <Dropdown
              role="Software Developer"
              position="Reality AI Lab"
              startDate="Feb"
              endDate="Apr 2025"
              src="/static/companies/realityai.png"
              description="Building full-stack systems for Marvel AI and Sky AI, using React, Node.js, and Python with Firestore, Firebase, and Redis to manage data and real-time workflows."
            />
            <Dropdown
              role="Front-End Developer"
              position="AdeptEye"
              startDate="Sep 2024"
              endDate="Apr 2025"
              src="/static/companies/adepteye.jfif"
              description="Revamped and optimized client websites on Shopify and Squarespace, improving UX, reducing load times by 40–50%, and launching scalable e-commerce platforms with POS integration and 1,800+ page views in the first week."
            />
            <Dropdown
              role="AI Engineer"
              position="Outlier AI"
              startDate="Mar 2024"
              endDate="Apr 2025"
              src="/static/companies/outlier.png"
              description="Developed a recursive self-improvement method that reduced trend-based LLM errors by 15–20%, enhancing reasoning through failure-based prompt refinement. Optimized AI response pipelines by analyzing 30–50 outputs per session, leveraging A/B testing, hallucination detection, and effectiveness evaluation to boost accuracy."
            />
          </div>
        </section>

        <section id="experience" className="flex flex-col">
          <p className="w-fit border border-gray-300 rounded-md px-2 py-1 text-xs uppercase my-10 font-semibold tracking-wider lg:py-[.5px] lg:text-sm">
            tech stack
          </p>
          <Marquee />
          <div className="mb-8" />
        </section>

        <section id="projects">
          <p className="w-fit border border-gray-300 rounded-md px-2 py-1 text-xs uppercase mt-10 mb-5 font-semibold tracking-wider lg:py-[.5px] lg:text-sm">
            projects
          </p>
          <Carousel />
        </section>

        <section id="education">
          <p className="w-fit border border-gray-300 rounded-md px-2 py-1 text-xs uppercase mt-10 mb-5 font-semibold tracking-wider lg:py-[.5px] lg:text-sm">
            education
          </p>
          <div className="flex flex-col gap-4">
            <Dropdown
              role="UCLA"
              position="Junior Level Transfer"
              startDate="Sep 2025"
              endDate="Present"
              src="/static/schools/ucla.png"
            />
            <Dropdown
              role="Mount San Antonio College"
              position="Honors Student"
              startDate="Jun 2023"
              endDate="Jun 2025"
              src="/static/schools/mtsac.png"
              description="Outreach Officer & Front-End Developer for the Computer Science Club."
            />
            <Dropdown
              role="Walnut High School"
              position="High School Diploma"
              startDate="Aug 2019"
              endDate="May 2023"
              src="/static/schools/whs.png"
            />
          </div>
        </section>
      </main>
    </div>
  );
}
