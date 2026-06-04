import { createBrowserRouter, Navigate } from 'react-router-dom';

import { AppShell } from '../layout/AppShell';
import { DashboardRoutePage } from './DashboardRoutePage';
import { ShipmentDetailPage } from './ShipmentDetailPage';
import { InboxPage } from '@/features/inbox';
import { ShipmentsListPage } from '@/features/shipments';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <DashboardRoutePage /> },
      { path: 'inbox', element: <InboxPage /> },
      { path: 'shipments', element: <ShipmentsListPage /> },
      { path: 'shipments/:id', element: <ShipmentDetailPage /> },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
]);
