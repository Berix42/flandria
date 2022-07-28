import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getImagePath } from '../../../helpers';

const MobileMenuSection = ({ header, children }) => (
  <div className="py-2">
    <h5 className="mb-1 text-sm font-bold tracking-wide text-slate-900 uppercase dark:text-white">
      {header}
    </h5>
    <ul>
      {children}
    </ul>
  </div>
);

const MobileMenuLink = ({
  to, children, external, onClick,
}) => {
  const className = 'text-sm font-semibold text-slate-500 hover:text-slate-900 dark:text-white dark:hover:text-dark-primary';

  if (external) {
    return (
      <li>
        <a
          className={className}
          href={to}
          target="_blank"
          rel="noreferrer"
        >
          {children}
        </a>
      </li>
    );
  }

  return (
    <li>
      <Link className={className} to={to} onClick={onClick}>
        {children}
      </Link>
    </li>
  );
};

const MobileSideMenu = ({ closeMenu, isLoggedIn }) => (
  <>
    <div className="fixed inset-y-0 left-0 z-50 sm:w-8/12 max-w-xs px-2 overflow-auto bg-white divide-y dark:bg-dark-2 dark:divide-dark-3">
      <img className="w-auto h-24 p-2" src={getImagePath('logo.png')} alt="Florensia Logo" />
      <MobileMenuSection header="Navigation">
        <MobileMenuLink to="/database/monster" onClick={closeMenu}>Monsters</MobileMenuLink>
        <MobileMenuLink to="/database" onClick={closeMenu}>Items</MobileMenuLink>
        <MobileMenuLink to="/database/quest" onClick={closeMenu}>Quests</MobileMenuLink>
      </MobileMenuSection>
      <MobileMenuSection header="Planner">
        <MobileMenuLink to="/planner/explorer" onClick={closeMenu}>Explorer</MobileMenuLink>
        <MobileMenuLink to="/planner/noble" onClick={closeMenu}>Noble</MobileMenuLink>
        <MobileMenuLink to="/planner/saint" onClick={closeMenu}>Saint</MobileMenuLink>
        <MobileMenuLink to="/planner/mercenary" onClick={closeMenu}>Mercenary</MobileMenuLink>
        <MobileMenuLink to="/planner/ship" onClick={closeMenu}>Ship</MobileMenuLink>
      </MobileMenuSection>
      <MobileMenuSection header="More">
        <MobileMenuLink to="/map" onClick={closeMenu}>Maps</MobileMenuLink>
        <MobileMenuLink to="/database/npc" onClick={closeMenu}>NPCs</MobileMenuLink>
        <MobileMenuLink to="/ranking/guilds" onClick={closeMenu}>Guilds Ranking</MobileMenuLink>
        <MobileMenuLink to="/static/files/essence_system_en.pdf" external>[EN] Essence Guide</MobileMenuLink>
        <MobileMenuLink to="/static/files/essence_system_de.pdf" external>[DE] Essence Guide</MobileMenuLink>
      </MobileMenuSection>
      <MobileMenuSection header="Account">
        {isLoggedIn
          ? (
            <MobileMenuLink to="/auth/logout" onClick={closeMenu}>Logout</MobileMenuLink>
          )
          : (
            <>
              <MobileMenuLink to="/auth/register" onClick={closeMenu}>Sign Up</MobileMenuLink>
              <MobileMenuLink to="/auth/login" onClick={closeMenu}>Sign In</MobileMenuLink>
            </>
          )}
      </MobileMenuSection>
    </div>
    <div
      onClick={closeMenu}
      role="button"
      aria-hidden="true"
      className="fixed inset-0 bg-black opacity-30"
    />
  </>
);

const MobileMenuButton = ({ buttonClassName, isLoggedIn }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleKeydown = (event) => {
    if (event.key === 'Escape') {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeydown);
  }, [isOpen]);

  return (
    <>
      <button className={buttonClassName} type="button" onClick={() => setIsOpen(!isOpen)}>
        <svg className="w-8 h-8 text-slate-700 dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      {isOpen && (
        <MobileSideMenu
          isLoggedIn={isLoggedIn}
          closeMenu={() => setIsOpen(false)}
        />
      )}
    </>
  );
};

export default MobileMenuButton;
