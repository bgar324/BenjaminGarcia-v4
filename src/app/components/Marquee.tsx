"use client";

import React, { useEffect, useRef } from 'react';

interface MarqueeProps {
  speed?: number;
  className?: string;
}

const Marquee: React.FC<MarqueeProps> = ({ 
  speed = -30,
  className = ""
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  const techImages = [
    { src: "/static/tech/react.png", alt: "React" },
    { src: "/static/tech/next.svg", alt: "Next.js" },
    { src: "/static/tech/javascript.png", alt: "JavaScript" },
    { src: "/static/tech/tailwind.png", alt: "Tailwind CSS" },
    { src: "/static/tech/bootstrap.png", alt: "Bootstrap" },
    { src: "/static/tech/c++.png", alt: "C++" },
    { src: "/static/tech/html.webp", alt: "HTML5" },
    { src: "/static/tech/python.webp", alt: "Python" }
  ];

  useEffect(() => {
    if (!containerRef.current || !contentRef.current) return;
    
    const container = containerRef.current;
    const content = contentRef.current;

    const clone = content.cloneNode(true) as HTMLDivElement;
    container.appendChild(clone);
    
    let position = 0;
    let lastTimestamp = performance.now();
    
    const animate = (timestamp: number) => {
      const delta = timestamp - lastTimestamp;
      lastTimestamp = timestamp;
    
      position += speed * (delta / 1000);
    
      if (position <= -content.offsetWidth) {
        position = 0;
      }
    
      container.style.transform = `translateX(${position}px)`;
      requestAnimationFrame(animate);
    };
    
    const animation = requestAnimationFrame(animate);
    
    
    return () => {
      cancelAnimationFrame(animation);
    };
  }, [speed]);

  return (
    <div className={`overflow-hidden whitespace-nowrap relative ${className}`}>
      <div className="absolute -left-0.5 top-0 h-full w-24 bg-gradient-to-r from-[#f7f6f7] to-transparent z-10"></div>
      
      <div 
        ref={containerRef} 
        className="inline-block"
        style={{ willChange: 'transform' }}
      >
        <div ref={contentRef} className="inline-block">
          {techImages.map((image, index) => (
            <img
              key={index}
              src={image.src}
              alt={image.alt}
              className="inline-block h-12 w-auto mx-8" 
            />
          ))}
        </div>
      </div>

      <div className="absolute -right-0.5 top-0 h-full w-24 bg-gradient-to-l from-[#f7f6f7] to-transparent z-10"></div>
    </div>
  );
};

export default Marquee;