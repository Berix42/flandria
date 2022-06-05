import React from 'react';
import { Link } from 'react-router-dom';

const Card = ({
  header, children, className, refObject,
}) => (
  <div ref={refObject} className={`flex flex-col bg-white border border-slate-200 rounded-md dark:bg-dark-3 dark:border-dark-4 ${className}`}>
    {header}
    {children}
  </div>
);

const CardHeader = ({ children }) => (
  <div className="px-4 py-2 border-b-2 border-slate-200 dark:border-dark-4">
    {children}
  </div>
);

const CardHeaderTitle = ({ children }) => (
  <h2 className="text-lg font-bold tracking-wide text-slate-600 dark:text-white">
    {children}
  </h2>
);

const ClickableCardItem = ({ children, to }) => (
  <Link
    to={to}
    className="block px-4 py-2 text-slate-700 cursor-pointer hover:bg-slate-100 hover:text-slate-900 dark:text-white dark:hover:bg-dark-4"
  >
    {children}
  </Link>
);

export default Card;
export {
  ClickableCardItem, CardHeader, CardHeaderTitle,
};
