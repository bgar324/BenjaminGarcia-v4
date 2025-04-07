"use client"

import React, { useState } from 'react';
import ProjectCard from './ProjectCard';
import { NavDown } from '../svgs/Icons';
import { motion, AnimatePresence } from 'framer-motion'

const projects = [
  {
    title: "Benjamin Garcia",
    description: "Portfolio website built with Next.js and Tailwind CSS, highlighting performance and being as lightweight as possible.",
    imageSrc: "/static/project-previews/portfoliov5.png",
    projectLink: "https://benjamin-garcia-v4.vercel.app/",
    technologies: ["Next.js", "Typescript", "Tailwind"]
  },
  {
    title: "15th Annual Health Professions Conference Website",
    description: "Developed a mobile-first website for Mt. SAC's 15th Annual Health Professions Conference. Designed to help attendees quickly access and submit feedback forms for each session.",
    imageSrc: "/static/project-previews/caduceus.png",
    projectLink: "https://github.com/bgar324/caduceus-club-website",
    technologies: ["Next", "Typescript", "Tailwind", "Vercel"]
  },
  {
    title: "Mt. SAC Computer Science Club Website",
    description: "Redesigned and developed the Mt. SAC Computer Science Club website using React.JS and Bootstrap to improve functionality, accessibility, and responsiveness. The site serves as a hub for members, providing resources, event details, officer contacts, and Discord access.",
    imageSrc: "/static/project-previews/csclubwebsite-preview.png",
    projectLink: "https://mtsaccs.netlify.app/",
    technologies: ["React", "Boostrap", "Netlify"]
  },
  {
    title: "logit",
    description: "A full-stack workout logging app designed for a minimal and efficient tracking experience. Users can log workouts, edit past sessions with a React-calendar, and track progress with Recharts visualizations. Workouts are stored in a PostgreSQL database, with support for tags, comments, and dropsets. Built with Next.js, Tailwind CSS, and Prisma, it streamlines workout management while enabling progressive overload tracking.",
    imageSrc: "/static/project-previews/logit-preview.png",
    projectLink: "https://github.com/bgar324/logit",
    technologies: ["Next", "React", "Tailwind", "react-calendar", "Recharts", "Supabase", "PostgreSQL", "Prisma"]
  },
  {
    title: "Roadmap Maker",
    description: "Built a CRUD web app using Next.js, Tailwind, and an MUI Timeline for visualizing tasks throughout the year. Users pick a month, define date ranges, and enter a title with an optional description, automatically placing tasks on the timeline. Integrated pdfmake enables generating a downloadable PDF of the entire roadmap.",
    imageSrc: "/static/project-previews/image.png",
    projectLink: "https://github.com/bgar324/roadmapMaker",
    technologies: ["Next", "Tailwind", "Material UI", "pdfmake"]
  },
  {
    title: "Tea Spots",
    description: "Collaborated with video production and graphic design teams to redesign a client's website using Square Online, integrating custom CSS, embedded code, and POS systems to support high traffic and dozens of weekly orders. Optimized multimedia assets for a cohesive, brand-aligned experience, resulting in thousands of page views and 200+ unique visits in the first week.",
    imageSrc: "/static/project-previews/teaspots.png",
    projectLink: "https://www.myteaspots.com/",
    technologies: ["Square Online", "Square Sites", "Photopea", "Graphic Design", "Video Production"]
  },
  {
    title: "Suika Remake",
    description: "Developed a physics-driven puzzle game featuring realistic ball dynamics using Pymunk, with color-coded merging mechanics and interactive player controls. Integrated gameplay elements like a scoring system, cooldown mechanics, and responsive visuals. Built with Pygame for rendering and Python for game logic and functionality.",
    imageSrc: "/static/project-previews/suika-preview.png",
    projectLink: "https://github.com/bgar324/suika",
    technologies: ["Python", "Pygame", "Pymunk"]
  },
  {
    title: "Weather Display",
    description: "Used OpenWeather's API in order to retrieve live data within the week based on the user's location. Created a simple front end with HTML & CSS, while using JavaScript to fetch the data and display it on the page.",
    imageSrc: "/static/project-previews/weather-preview.jfif",
    projectLink: "https://beautiful-gumption-a0ca0e.netlify.app/",
    technologies: ["HTML", "CSS", "JavaScript", "OpenWeather API"]
  },
];

const Carousel: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  // Calculate the number of sections (2 projects per section)
  const totalSections = Math.ceil(projects.length / 2);
  
  const goToNextSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === totalSections - 1 ? 0 : prevIndex + 1
    );
  };
  
  const goToPrevSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === 0 ? totalSections - 1 : prevIndex - 1
    );
  };
  
  // Get current projects to display (2 per section)
  const startIdx = currentIndex * 2;
  const currentProjects = projects.slice(startIdx, startIdx + 2);
  
  return (
    <div className="relative w-full">
      {totalSections > 1 && (
        <div className="flex justify-between mb-4">
          <button 
            onClick={goToPrevSlide}
            className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            aria-label="Previous projects"
          >
            <div className="transform rotate-90">
              <NavDown />
            </div>
          </button>
          
          <button 
            onClick={goToNextSlide}
            className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            aria-label="Next projects"
          >
            <div className="transform -rotate-90">
              <NavDown />
            </div>
          </button>
        </div>
      )}
      
      <AnimatePresence mode="wait">
        <motion.div
          key={currentIndex}
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -100, opacity: 0 }}
          transition={{ duration: 0.25 }}
          className="flex flex-row gap-3 my-4"
        >
          {currentProjects.map((project, index) => (
            <div key={startIdx + index} className="w-1/2">
              <ProjectCard
                title={project.title}
                description={project.description}
                imageSrc={project.imageSrc}
                projectLink={project.projectLink}
                technologies={project.technologies}
              />
            </div>
          ))}
        </motion.div>
      </AnimatePresence>
      
      {totalSections > 1 && (
        <div className="flex justify-center mt-4">
          <div className="flex gap-2 items-center">
            {Array.from({ length: totalSections }).map((_, idx) => (
              <span 
                key={idx} 
                className={`h-2 w-2 rounded-full ${idx === currentIndex ? 'bg-gray-800' : 'bg-gray-300'}`}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Carousel;