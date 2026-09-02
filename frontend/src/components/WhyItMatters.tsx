import React from 'react';
import { topics } from '../data/content';

export function WhyItMatters() {
  const [first, second, third] = topics;

  return (
    <section
      id="why-deepfakes"
      aria-labelledby="matters-heading"
      className="scroll-mt-16 border-b border-rule">
      
      <div className="mx-auto max-w-spread px-5 py-12 sm:px-8 lg:px-12 lg:py-20">
        <p className="border-b border-ink pb-2 font-mono text-[10px] uppercase tracking-label text-ink">
          Why deepfakes matter
        </p>

        <h2
          id="matters-heading"
          className="mt-7 max-w-[22ch] font-display uppercase leading-[0.93] tracking-[-0.015em] text-ink"
          style={{ fontSize: 'clamp(2.3rem, 5.4vw, 5rem)' }}>
          
          The image may be {' '}
          <span className='italic lowercase'> fake </span>
          <br />
          The consequences{' '}
          <span className="italic lowercase">aren&rsquo;t.</span>
        </h2>

        {/* Lead topic — given the most space because it is the broadest harm */}
        <div className="mt-12 grid gap-8 lg:grid-cols-12 lg:gap-14">
          <figure className="lg:col-span-7">
            <div className="paper-grain bg-ivorydeep">
              <img
                src={first.image}
                alt="Newspapers stacked on a wet pavement at dusk."
                className="h-[240px] w-full object-cover sm:h-[340px]" />
              
            </div>
            <figcaption className="mt-3 border-t border-rule pt-2 font-mono text-[10px] uppercase tracking-label text-gray-soft">
              {first.caption}
            </figcaption>
          </figure>
          <div className="lg:col-span-5 lg:pt-6">
            <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
              {first.index}
            </p>
            <h3 className="mt-2 font-display text-[32px] uppercase leading-none tracking-[-0.01em] text-ink lg:text-[40px]">
              {first.title}
            </h3>
            <p className="mt-4 max-w-[44ch] text-[16px] leading-[1.65] text-graphite">
              {first.body}
            </p>
          </div>
        </div>

        {/* Two supporting topics, offset against each other */}
        <div className="mt-14 grid gap-10 border-t border-rule pt-10 lg:grid-cols-12 lg:gap-14">
          <div className="lg:col-span-5">
            <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
              {second.index}
            </p>
            <h3 className="mt-2 font-display text-[28px] uppercase leading-none tracking-[-0.01em] text-ink">
              {second.title}
            </h3>
            <p className="mt-4 max-w-[42ch] text-[15px] leading-[1.65] text-graphite">
              {second.body}
            </p>
            <figure className="mt-6">
              <div className="paper-grain bg-ivorydeep">
                <img
                  src={second.image}
                  alt="An empty chair beside a contact sheet of portraits pinned to a wall."
                  className="h-[220px] w-full object-cover sm:h-[260px]" />
                
              </div>
              <figcaption className="mt-3 border-t border-rule pt-2 font-mono text-[10px] uppercase tracking-label text-gray-soft">
                {second.caption}
              </figcaption>
            </figure>
          </div>

          <div className="lg:col-span-6 lg:col-start-7 lg:pt-24">
            <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
              {third.index}
            </p>
            <h3 className="mt-2 font-display text-[28px] uppercase leading-none tracking-[-0.01em] text-ink">
              {third.title}
            </h3>
            <p className="mt-4 max-w-[42ch] text-[15px] leading-[1.65] text-graphite">
              {third.body}
            </p>
            <figure className="mt-6">
              <div className="paper-grain bg-ivorydeep">
                <img
                  src={third.image}
                  alt="Hands holding a phone displaying an indistinct photograph."
                  className="h-[220px] w-full object-cover sm:h-[300px]" />
                
              </div>
              <figcaption className="mt-3 border-t border-rule pt-2 font-mono text-[10px] uppercase tracking-label text-gray-soft">
                {third.caption}
              </figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>);

}