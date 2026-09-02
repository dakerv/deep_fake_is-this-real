import React from 'react';

const considerations = [
{
  label: 'Context',
  body: 'Where the image appeared, and what claim it is being used to support.'
},
{
  label: 'Source',
  body: 'Who published it first, and whether that origin can be established.'
},
{
  label: 'Corroboration',
  body: 'Whether independent reporting or other imagery supports the same event.'
}];


export function ResponsibleUse() {
  return (
    <section
      id="responsible-use"
      aria-labelledby="responsible-heading"
      className="scroll-mt-16">
      
      <div className="mx-auto max-w-spread px-5 py-12 sm:px-8 lg:px-12 lg:py-16">
        <p className="border-b border-ink pb-2 font-mono text-[10px] uppercase tracking-label text-ink">
          Responsible use
        </p>

        <div className="mt-7 grid gap-8 lg:grid-cols-12 lg:gap-14">
          <h2
            id="responsible-heading"
            className="font-display uppercase leading-[0.95] tracking-[-0.015em] text-ink lg:col-span-5"
            style={{ fontSize: 'clamp(2rem, 3.6vw, 3.4rem)' }}>
            
            A detector is not a{' '}
            <span className="italic lowercase">verdict.</span>
          </h2>

          <div className="lg:col-span-7">
            <p className="max-w-[62ch] text-[16px] leading-[1.7] text-graphite">
              This model returns a probability, not a fact. At times, it can be confident
              and wrong on unfamiliar image types, heavy compression, unusual
              lighting, or manipulation methods it has never encountered. Treat
              a classification as one piece of evidence among several, and weigh
              it against everything else you can establish about the image.
            </p>

            <ul className="mt-8 divide-y divide-rule border-t border-rule">
              {considerations.map((item) =>
              <li key={item.label} className="grid gap-2 py-4 sm:grid-cols-12">
                  <span className="font-mono text-[10px] uppercase tracking-label text-ink sm:col-span-3">
                    {item.label}
                  </span>
                  <span className="text-[15px] leading-[1.6] text-graphite sm:col-span-9">
                    {item.body}
                  </span>
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </section>);

}