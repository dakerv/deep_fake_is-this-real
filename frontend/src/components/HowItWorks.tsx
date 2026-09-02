import React from 'react';
import { workSteps } from '../data/content';

export function HowItWorks() {
  return (
    <section
      id="how-it-works"
      aria-labelledby="how-heading"
      className="scroll-mt-16 border-b border-rule">
      
      <div className="mx-auto max-w-spread px-5 py-12 sm:px-8 lg:px-12 lg:py-16">
        <div className="grid gap-8 lg:grid-cols-12 lg:gap-14">
          <div className="lg:col-span-3">
            <h2
              id="how-heading"
              className="font-display uppercase leading-[0.95] tracking-[-0.01em] text-ink"
              style={{ fontSize: 'clamp(1.9rem, 3vw, 2.9rem)' }}>
              
              How it works
            </h2>
            <dl className="mt-6 space-y-2 border-t border-rule pt-3">
              <div className="flex gap-2">
                <dt className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
                  Model /
                </dt>
                <dd className="font-mono text-[10px] uppercase tracking-label text-ink">
                  EfficientNet-B0
                </dd>
              </div>
              <div className="flex gap-2">
                <dt className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
                  Classification /
                </dt>
                <dd className="font-mono text-[10px] uppercase tracking-label text-ink">
                  3 classes
                </dd>
              </div>
            </dl>
          </div>

          <ol className="grid gap-0 border-t border-ink lg:col-span-9 lg:grid-cols-4 lg:border-t">
            {workSteps.map((step, i) =>
            <li
              key={step.index}
              className={`border-b border-rule py-5 lg:border-b-0 lg:py-0 lg:pb-2 lg:pt-4 ${
              i > 0 ? 'lg:border-l lg:border-rule lg:pl-5' : 'lg:pr-5'} ${
              i > 0 && i < 3 ? 'lg:pr-5' : ''}`}>
              
                <p className="font-mono text-[10px] uppercase tracking-label text-gray-soft">
                  {step.index} /
                </p>
                <h3 className="mt-2 font-display text-[26px] uppercase leading-none tracking-[-0.01em] text-ink lg:text-[30px]">
                  {step.title}
                </h3>
                <p className="mt-3 max-w-[30ch] text-[14px] leading-[1.6] text-graphite">
                  {step.body}
                </p>
              </li>
            )}
          </ol>
        </div>
      </div>
    </section>);

}