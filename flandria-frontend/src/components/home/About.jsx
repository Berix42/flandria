import React, { useEffect } from 'react';
import { setWindowTitle } from '../../helpers';
import Prose from '../shared/Prose';

const About = () => {
  useEffect(() => {
    setWindowTitle('About');
  }, []);

  return (
    <Prose>
      <h1 className="sr-only">About</h1>
      <h2>What is Flandria?</h2>
      <p>
        Flandria is a project that started late 2018 with the goal to make a good
        Florensia database website. It was then first released on the first of January 2019.
        <br />
        Even today, it is still in development and maintained on a regular basis to reflect
        the newest patches.
        <br />
        The development of the original project by
        {' '}
        <a href="https://github.com/HealYouDown/flandria">Jeremy</a>
         was stopped on 01.01.2022.
        This website is is a fork of the original project, which is now hosted by
        {' '}
        <a href="https://www.giikugames.com">Giiku Games</a>
         and presents a continued effort by the community to
        keep development going.
      </p>

      <h2>How does Flandria work?</h2>
      <p>
        Obviously, adding all information manually would require months, keeping them up to
        date even more.
        <br />
        Therefore, Flandria takes all its data (except drops) from the game client. This is
        done fully automatically.
        <br />
        <blockquote>
          Credits go to
          {' '}
          <a href="https://github.com/Flauschbaellchen">Noxx</a>
          , which scripts were available on Github and allowed me to
          implement those algorithms without having to figure everything out
          from scratch.
        </blockquote>
      </p>
      <h3>Stack</h3>
      <p>
        Flandria consists of a Frontend and Backend that are seperated from each other -
        the backend is written in
        {' '}
        <a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a>
        ,
        while the Frontend uses
        {' '}
        <a href="https://reactjs.org/">ReactJS</a>
        .
      </p>
      <h3>Github</h3>
      <p>
        Flandria is completly open-source and avaialable on Github.
        You are free to contribute.
        <br />
        If you have no coding experience but want to help out, you can
        do this by joining our
        {' '}
        <a href="https://discord.gg/GiikuGames">Discord</a>
        {' '}
        and help us collect all the (still)
        missing drops.
      </p>
    </Prose>
  );
};

export default About;
