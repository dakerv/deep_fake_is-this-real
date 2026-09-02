import React from 'react';

export function Footer() {
  return (
    <footer className="border-t border-rule">
      <div className="mx-auto flex max-w-spread flex-col gap-4 px-5 py-8 sm:flex-row sm:items-baseline sm:justify-between sm:px-8 lg:px-12">
        <p className="font-display text-[20px] leading-none tracking-[-0.01em] text-ink">
          IS THIS REAL?
        </p>
        <p className="max-w-[52ch] font-mono text-[10px] uppercase leading-[1.7] tracking-label text-gray-soft">
          An editorial examination of digital image authenticity. No account
          required · Images are not retained · Model / EfficientNet-B0
        </p>
      </div>
    </footer>);

}