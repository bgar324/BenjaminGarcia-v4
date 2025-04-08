import React from "react";
import { ArrowUpRight } from "../svgs/Icons";
import Image from "next/image";

const PastVersions = () => {
  const versions = [
    {
      link: "https://v1benjamingarcia.vercel.app/",
      favicon: "/static/previous favicons/faviconv1.png",
      version: 1,
    },
    {
      link: "https://v2benjamingarcia.vercel.app/",
      favicon: "/static/previous favicons/faviconv2.png",
      version: 2,
    },
    {
      link: "https://v3benjamingarcia.vercel.app/",
      favicon: "/static/previous favicons/faviconv3.png",
      version: 3,
    },
  ];

  return (
    <div className="w-full grid grid-cols-2 gap-1">
      {versions.slice(0, 2).map((item, index) => (
        <a
          key={index}
          href={item.link}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-x-2 text-gray-900 hover:bg-[#f6f7f7] transition-colors duration-300 bg-white border border-dotted border-gray-300 rounded-lg px-4 py-2"
        >
          <span className="flex items-center">
            <Image
              src={item.favicon}
              alt={`v${item.version} favicon`}
              width={16}
              height={16}
              className="mr-2"
            />
            v{item.version}
          </span>
          <ArrowUpRight />
        </a>
      ))}
      <a
        href={versions[2].link}
        target="_blank"
        rel="noopener noreferrer"
        className="col-span-2 flex items-center justify-center gap-x-2 text-gray-900 hover:bg-[#f6f7f7] transition-colors duration-300 bg-white border border-dotted border-gray-300 rounded-lg px-4 py-2"
      >
        <span className="flex items-center">
          <Image
            src={versions[2].favicon}
            alt={`v${versions[2].version} favicon`}
            width={16}
            height={16}
            className="mr-2"
          />
          v{versions[2].version}
        </span>
        <ArrowUpRight />
      </a>
    </div>
  );
};

export default PastVersions;
