import React from 'react'
import { ArrowUpRight } from '../svgs/Icons'

const PastVersions = () => {
  const versions = [
    "https://v1benjamingarcia.vercel.app/",
    "https://v2benjamingarcia.vercel.app/",
    "https://v3benjamingarcia.vercel.app/"
  ]

  return (
    <div className="flex flex-row flex-wrap mx-auto justify-center items-center gap-4">
      {versions.map((link, index) => (
        <a 
          key={index}
          href={link}
          target="_blank"
          rel="noopener noreferrer" 
          className="flex items-center gap-x-2 text-gray-900 hover:bg-[#f6f7f7] transition-colors duration-300 bg-white border border-dotted border-gray-300 rounded-lg px-14"
        >
          <span>v{index + 1}</span>
          <ArrowUpRight />
        </a>
      ))}
    </div>
  )
}

export default PastVersions