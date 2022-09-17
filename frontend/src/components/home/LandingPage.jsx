import React from 'react';
import { getImagePath, setWindowTitle } from '../../helpers';
import { apiUrl } from '../../constants';

const LandingPage = () => {
  setWindowTitle('Home');

  return (
    <div className="flex flex-col items-center justify-center gap-y-10 lg:gap-20 lg:flex-row">
      <div className="max-w-3xl">
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-gray-700 lg:text-5xl dark:text-white">Welcome to Flandria</h1>
        <h2 className="text-lg ml-1 mb-5 tracking-wide text-gray-500 dark:text-white dark:text-opacity-90">Your Florensia Database</h2>
        <p className="max-w-lg ml-1 text-base font-thin leading-7 text-gray-500 dark:text-white dark:text-opacity-70">
          Flandria is an open-source database website for the MMORPG Florensia.
          It provides a clean interface for you to browse through all monsters, items and quests
          that exist in the world of Florensia.
          Also included are a character builder which allows you to design your own character
          skilltree, as well as a list of all players and guilds across all servers!
          The data of Flandria is publicly available. If you are interested in it then check out
          {' '}
          <a
            href={apiUrl}
            target="_blank"
            rel="noreferrer"
            className="underline decoration-sky-500 hover:text-blue-800 hover:font-semibold dark:hover:text-blue-300"
          >
            Flandria API
          </a>
        </p>
      </div>

      <div className="max-w-md grid grid-cols-2 gap-4">
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiExploF.png')} alt="Explorer Female" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiExploM.png')} alt="Explorer Male" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiMercF.png')} alt="Mercenary Female" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiMercM.png')} alt="Mercenary Male" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiNobF.png')} alt="Noble Female" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiNobM.png')} alt="Noble Male" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiSaintF.png')} alt="Saint Female" />
        <img className="rounded-full h-32" src={getImagePath('chibis/1207xx_FLO_chibiSaintM.png')} alt="Saint Male" />
      </div>
    </div>
  );
};

export default LandingPage;
