import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const anchors = [
{ label: 'How it works', hash: 'how-it-works' },
{ label: 'Why deepfakes matter', hash: 'why-deepfakes' },
{ label: 'Responsible use', hash: 'responsible-use' }];


export function Header() {
  const navigate = useNavigate();
  const location = useLocation();

  const goToDetection = () => {
    if (location.pathname !== '/') navigate('/');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const separator =
  <span aria-hidden="true" className="px-2 text-[11px] text-gray-soft sm:px-3">
      ·
    </span>;


  return (
    <header className="sticky top-0 z-40 border-b border-rule bg-ivory/95 backdrop-blur-[2px]">
      <div className="mx-auto flex max-w-spread flex-col gap-1.5 px-5 py-3 sm:flex-row sm:items-baseline sm:justify-between sm:gap-6 sm:px-8 lg:px-12">
        <button
          type="button"
          onClick={goToDetection}
          className="self-start font-display text-[19px] leading-none tracking-[-0.01em] text-ink sm:text-[23px]">
          
          IS THIS REAL?
        </button>

        <nav
          aria-label="Sections"
          className="-mx-1 flex items-baseline overflow-x-auto px-1 sm:mx-0 sm:overflow-visible sm:px-0">
          
          <button
            type="button"
            onClick={goToDetection}
            className="hairline-underline whitespace-nowrap text-[11px] text-graphite sm:text-[13px]">
            
            Detection
          </button>
          {anchors.map((item) =>
          <React.Fragment key={item.hash}>
              {separator}
              <a
              href={`#${item.hash}`}
              className="hairline-underline whitespace-nowrap text-[11px] text-graphite sm:text-[13px]">
              
                {item.label}
              </a>
            </React.Fragment>
          )}
        </nav>
      </div>
    </header>);

}