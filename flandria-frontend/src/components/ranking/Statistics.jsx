import React, { useEffect, useState } from 'react';
import TopBarProgress from 'react-topbar-progress-indicator';
import useAsyncError from '../errors/useAsyncError';
import CharacterCountBarChart from './charts/CharacterCountBarChart';
import CharacterCountPieCharts from './charts/CharacterCountPieCharts';
import { getStatistics } from '../../services/RankingService';

const Statistics = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);
  const [minLevelLand] = useState(1);

  const throwError = useAsyncError();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getStatistics(`min_level_land=${minLevelLand}`);
        setData(result.data);
        setIsLoading(false);
      } catch (error) {
        throwError(new Error(error));
      }
    };

    setIsLoading(true);
    fetchData();
  }, [minLevelLand]);

  if (isLoading) return <TopBarProgress />;

  return (
    <div className="flex flex-col gap-4">
      <span className="text-3xl font-semibold text-slate-700 dark:text-white">
        Minimum Land Level:
        {' '}
        {minLevelLand}
      </span>
      <CharacterCountBarChart data={data.character_counts.counts} />
      <CharacterCountPieCharts data={data.character_counts} />
    </div>
  );
};

export default Statistics;
