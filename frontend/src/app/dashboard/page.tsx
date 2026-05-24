"use client";
import { useEffect, useState } from "react";
import { MetricsCard } from "@/components/dashboard/MetricsCard";
import { AgentStatusGrid } from "@/components/dashboard/AgentStatusGrid";
import { ActivityFeed } from "@/components/dashboard/ActivityFeed";
import { api, type DashboardSummary } from "@/lib/api";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<DashboardSummary>("/dashboard/summary")
      .then(setSummary)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-white">Dashboard</h1>

      <div className="grid grid-cols-4 gap-4">
        <MetricsCard title="Tasks Today" value={summary?.tasks_today_total ?? 0} loading={loading} />
        <MetricsCard title="Completed" value={summary?.tasks_today_completed ?? 0} trend="up" loading={loading} />
        <MetricsCard title="Pending" value={summary?.tasks_today_pending ?? 0} loading={loading} />
        <MetricsCard title="Failed" value={summary?.tasks_today_failed ?? 0} trend={summary?.tasks_today_failed ? "down" : "neutral"} loading={loading} />
      </div>

      <AgentStatusGrid />

      <div className="h-80">
        <ActivityFeed />
      </div>
    </div>
  );
}
