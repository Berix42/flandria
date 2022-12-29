import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Select from 'react-select';
import TopBarProgress from 'react-topbar-progress-indicator';
import { setWindowTitle } from '../../helpers';
import useDidMountEffect from '../../useDidMountEffect';
import { getQueryParameterOrDefault } from '../database/TableView/TableView';
import TableViewItem from '../database/TableView/TableViewItem';
import useAsyncError from '../errors/useAsyncError';
import Breadcrumbs from '../shared/Breadcrumbs';
import Pagination from '../shared/Pagination';
import { getGuildsRanking } from '../../services/RankingService';

const serverSelectOptions = [
  {
    label: 'Both',
    value: 'both',
  },
  {
    label: 'Bergruen',
    value: 'bergruen',
  },
  {
    label: 'LuxPlena',
    value: 'luxplena',
  },
];

const GuildOverview = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const throwError = useAsyncError();

  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);

  const [currentPage, setCurrentPage] = useState(
    parseInt(getQueryParameterOrDefault('page', '1'), 10),
  );
  const [selectedServer, setSelectedServer] = useState(
    getQueryParameterOrDefault('server', 'both'),
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getGuildsRanking(new URLSearchParams(location.search).toString());

        setData({
          searchParams: location.search,
          data: result.data,
        });
        setIsLoading(false);
      } catch (error) {
        throwError(new Error(error));
      }
    };

    setIsLoading(true);
    fetchData();
  }, [location]);

  useDidMountEffect(() => {
    if (currentPage === 0) {
      // Reset page
      setCurrentPage(1);
      return;
    }

    const params = new URLSearchParams({
      page: currentPage,
      server: selectedServer,
    });

    const args = {
      pathname: location.pathname,
      search: `?${params.toString()}`,
    };

    navigate(args, { replace: !location.search });
  }, [currentPage]);

  useDidMountEffect(() => {
    setCurrentPage(0);
  }, [selectedServer]);

  useEffect(() => {
    setWindowTitle('Guilds Ranking');
  }, []);

  return (
    <>
      {isLoading && (<TopBarProgress />)}
      <div className="flex items-end justify-between pb-3 border-b border-slate-200 dark:border-dark-3">
        <div>
          <Breadcrumbs
            items={[
              { text: 'Ranking', url: '/' },
              { text: 'Guilds', url: '/ranking/guilds' },
            ]}
          />
          <div className="flex items-center mt-2">
            <h2 className="mt-0 text-2xl font-semibold text-slate-700 md:text-3xl dark:text-white">
              Guilds
            </h2>
          </div>
        </div>
        <Select
          classNamePrefix="react-select"
          className="w-40"
          options={serverSelectOptions}
          value={serverSelectOptions.filter((opt) => opt.value === selectedServer)}
          onChange={(opt) => setSelectedServer(opt.value)}
        />
      </div>
      <div className="mt-3">
        {(data && !isLoading && (data.searchParams === location.search)) && (
        <>
          <div className="grid grid-cols-1 gap-3 py-3 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {data.data.items.map((guild) => (
              <TableViewItem
                key={guild.name}
                tablename="guild"
                item={guild}
                showIcon={false}
              />
            ))}
          </div>
          <div className="flex flex-row justify-center pt-4">
            <Pagination
              currentPage={currentPage}
              hasPrevious={data.data.pagination.has_previous}
              hasNext={data.data.pagination.has_next}
              labels={data.data.pagination.labels}
              onPageChange={(newPage) => {
                setCurrentPage(newPage);
              }}
            />
          </div>
        </>
        )}
      </div>
    </>
  );
};

export default GuildOverview;