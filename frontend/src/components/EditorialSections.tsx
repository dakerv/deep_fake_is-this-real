import React from 'react';
import { FeaturedCase } from './FeaturedCase';
import { ImageTypes } from './ImageTypes';
import { HowItWorks } from './HowItWorks';
import { WhyItMatters } from './WhyItMatters';
import { ResponsibleUse } from './ResponsibleUse';

/**
 * The editorial body of the publication. It stays put beneath the detection
 * slot, whichever state of the flow is showing above it.
 */
export function EditorialSections() {
  return (
    <>
      <FeaturedCase />
      <ImageTypes />
      <HowItWorks />
      <WhyItMatters />
      <ResponsibleUse />
    </>);

}