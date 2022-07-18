import React from 'react';
import {
  BrowserRouter as Router, Route, Routes,
} from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { ErrorBoundary } from 'react-error-boundary';
import { CookiesProvider } from 'react-cookie';
import LoginView from './components/auth/LoginView';
import LogoutView from './components/auth/LogoutView';
import RegisterView from './components/auth/RegisterView';
import DetailedTableView from './components/database/DetailedTableView/DetailedTableView';
import ItemsOverview from './components/database/ItemsOverview';
import TableView from './components/database/TableView/TableView';
import Error404Page from './components/errors/404';
import About from './components/home/About';
import LandingPage from './components/home/LandingPage';
import LegalNotice from './components/home/LegalNotice';
import PrivacyPolicy from './components/home/PrivacyPolicy';
import Layout from './components/layout/Layout';
import MapsOverview from './components/map/MapsOverview';
import MapView from './components/map/MapView';
import PlannerView from './components/planner/PlannerView';
import GATracker from './GATracker';
import ErrorBoundaryView from './components/errors/ErrorBoundaryView';
import RankingStatistics from './components/ranking/Statistics';
import GuildOverview from './components/ranking/GuildOverview';
import GuildView from './components/ranking/GuildView';
import PlayerView from './components/ranking/PlayerView';
import PublishBuildView from './components/planner/PublishBuildView';
import BuildsView from './components/planner/BuildsView';

TopBarProgress.config({
  barColors: {
    '0.0': 'teal',
    '1.0': 'teal',
  },
  shadowBlur: 5,
});

const App = () => (
  <Router>
    <ErrorBoundary
      FallbackComponent={ErrorBoundaryView}
    >
      <GATracker trackingId="UA-216355284-1">
        <CookiesProvider>
          <Layout>
            <Routes>
              <Route path="/" exact element={<LandingPage />} />
              <Route path="/about" exact element={<About />} />
              <Route path="/privacy-policy" exact element={<PrivacyPolicy />} />
              <Route path="/legal-notice" exact element={<LegalNotice />} />

              <Route path="/auth/login" exact element={<LoginView />} />
              <Route path="/auth/register" exact element={<RegisterView />} />
              <Route path="/auth/logout" exact element={<LogoutView />} />

              <Route path="/database" exact element={<ItemsOverview />} />
              <Route path="/database/:tablename" exact element={<TableView />} />
              <Route path="/database/:tablename/:code" exact element={<DetailedTableView />} />

              <Route path="/map" exact element={<MapsOverview />} />
              <Route path="/map/:mapCode" exact element={<MapView />} />

              <Route path="/planner/:classname" exact element={<PlannerView />} />
              <Route path="/planner/:classname/builds" exact element={<BuildsView />} />
              <Route path="/planner/builds/add" exact element={<PublishBuildView />} />

              <Route path="/ranking/statistics" exact element={<RankingStatistics />} />
              <Route path="/ranking/guilds" exact element={<GuildOverview />} />
              <Route path="/ranking/guilds/:guildName+" exact element={<GuildView />} />
              <Route path="/ranking/players/:server/:name" exact element={<PlayerView />} />

              <Route path="*" element={<Error404Page />} />
            </Routes>
          </Layout>
        </CookiesProvider>
      </GATracker>
    </ErrorBoundary>
  </Router>
);

export default App;
