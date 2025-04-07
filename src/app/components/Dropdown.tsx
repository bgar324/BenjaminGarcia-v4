"use client";

import React, { useState } from "react";
import { NavDown, XIcon } from "../svgs/Icons";

interface DropdownProps {
  role: string;
  position: string;
  startDate: string;
  endDate: string;
  src: string;
  link?: string;
  description?: string;
}

const Dropdown: React.FC<DropdownProps> = ({
  role,
  position,
  startDate,
  endDate,
  src,
  link,
  description
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const hasExpandableContent = description || link;

  return (
    <div className="border border-gray-300 border-dotted bg-white rounded-lg flex flex-col">
      <div className="flex flex-row">
        <div className="flex justify-center items-center">
          <img
            src={src}
            className="h-auto w-16 rounded-xl bg-white items-center p-1 lg:ml-1"
          />
        </div>

        <div className="flex flex-col w-full p-2">
          <h1 className="font-semibold w-full lg:text-lg">{role}</h1>
          <div className="flex flex-row justify-between items-center">
            <div className="flex flex-row items-center">
              <p className="text-sm text-gray-600 lg:text-base">{position}</p>
              <p className="text-sm text-gray-600 ml-2 md:hidden">| <span className = "ml-1">{startDate} - {endDate}</span></p>
            </div>
            <div className="flex flex-row items-center">
              <p className="text-sm text-gray-600 hidden md:block lg:text-base">{startDate} - {endDate}</p>
              {hasExpandableContent && (
                <button 
                  onClick={toggleDropdown}
                  className="ml-2 transition-transform duration-300"
                >
                  {isOpen ? <XIcon /> : <NavDown />}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
      
      <div 
        className={`overflow-hidden transition-all duration-500 ease-in-out ${
          isOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
        style={{ 
          transitionTimingFunction: 'cubic-bezier(0.4, 0, 0.2, 1)'
        }}
      >
        {hasExpandableContent && (
          <div className="p-4 border-t border-gray-200">
            {description && <p className="text-sm lg:text-base text-gray-800">{description}</p>}
            {link && (
              <a 
                href={link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline text-sm mt-2 inline-block"
              >
                Visit website
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dropdown;
