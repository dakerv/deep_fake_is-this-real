import React from 'react';
import { imageTypes } from '../data/content';

export function ImageTypes() {
  return (
    <section aria-labelledby="types-heading" className="border-b border-rule">
      <div className="mx-auto max-w-spread px-5 py-12 sm:px-8 lg:px-12 lg:py-16">
        <div className="flex flex-wrap items-baseline justify-between gap-3 border-b border-ink pb-2">
          <h2
            id="types-heading"
            className="font-mono text-[10px] uppercase tracking-label text-ink">
            
            Three types of images
          </h2>
          <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
            Reference plates 02 — 04
          </p>
        </div>

        <ul className="mt-6 grid grid-cols-1 gap-x-8 gap-y-10 sm:grid-cols-3">
          {imageTypes.map((type) =>
          <li key={type.index} className="flex flex-col">
              <div className="flex items-baseline justify-between pb-2">
                <span className="font-mono text-[10px] uppercase tracking-label text-ink">
                  {type.index} — {type.label}
                </span>
              </div>
              <div className="paper-grain relative bg-ivorydeep">
                <img
                src={type.image}
                alt={`Example of a ${type.label.toLowerCase()} photograph.`}
                className="aspect-square w-full object-cover" />
              
              </div>
              <p className="mt-3 border-t border-rule pt-3 text-[15px] leading-[1.6] text-graphite">
                {type.caption}
              </p>
              <p className="mt-auto pt-3 font-mono text-[10px] uppercase tracking-label text-gray-soft">
                {type.credit}
              </p>
            </li>
          )}
        </ul>
      </div>
    </section>);

}