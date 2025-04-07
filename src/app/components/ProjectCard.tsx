import React, { useState } from 'react'
import { ArrowUpRight } from '../svgs/Icons'
import Image from 'next/image'

interface ProjectCardProps {
  title: string;
  description: string;
  imageSrc: string;
  projectLink?: string;
  technologies: string | string[];
}

const ProjectCard: React.FC<ProjectCardProps> = ({
  title,
  description,
  imageSrc,
  projectLink,
  technologies
}) => {
  const techArray = Array.isArray(technologies) ? technologies : [technologies];
  
  const [isExpanded, setIsExpanded] = useState(false);
  
  const maxChars = 100;
  
  const isTruncated = description.length > maxChars;
  const truncatedDescription = isTruncated && !isExpanded 
    ? `${description.substring(0, maxChars)}...` 
    : description;
  
  return (
    <div className="bg-white rounded-xl shadow-sm w-auto h-auto flex flex-col p-2">
      <div className="relative w-full" style={{ aspectRatio: '16/9' }}>
        <Image 
          src={imageSrc} 
          alt={title} 
          fill
          style={{ objectFit: 'cover' }}
          className="rounded-lg"
        />
      </div>
      <div className="flex flex-row gap-2 items-center mt-2">
        {projectLink ? (
          <a href={projectLink} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1">
            <h1 className = "font-medium hover:underline lg:text-base">{title}</h1>
            <ArrowUpRight />
          </a>
        ) : (
          <h1 className = "font-medium hover:underline lg:text-base">{title}</h1>
        )}
      </div>
      <div className="text-sm lg:text-base text-gray-600">
        <p>{truncatedDescription}</p>
        {isTruncated && (
          <button 
            onClick={() => setIsExpanded(!isExpanded)} 
            className="text-blue-500 hover:text-blue-700 text-xs mt-1 font-medium"
          >
            {isExpanded ? 'Show less' : 'Read more'}
          </button>
        )}
      </div>
      <div className="flex flex-wrap gap-2 mt-3">
        {techArray.map((tech, index) => (
          <span 
            key={index} 
            className="text-xs bg-gray-100 px-2 py-1 rounded-lg"
          >
            {tech}
          </span>
        ))}
      </div>
    </div>
  )
}

export default ProjectCard