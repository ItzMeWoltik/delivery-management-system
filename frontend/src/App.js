import React, { useContext } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { AuthContext } from './contexts/AuthContext';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import CreateOrder from './components/Customer/CreateOrder';
import OrderStatus from './components/Customer/OrderStatus';
import OrderHistory from './components/Customer/OrderHistory';
import CustomerChat from './components/Customer/CustomerChat';
import AvailableOrders from './components/Courier/AvailableOrders';
import ActiveOrders from './components/Courier/ActiveOrders';
import CourierOrderHistory from './components/Courier/OrderHistory';
import LocationUpdate from './components/Courier/LocationUpdate';
import CourierChat from './components/Courier/CourierChat';
import Dashboard from './components/Admin/Dashboard';
import Alerts from './components/Admin/Alerts';
import ManageOrders from './components/Admin/ManageOrders';
import GeoView from './components/Admin/GeoView';
import LanguageSelector from './components/Common/LanguageSelector';
import SupportTicket from './components/Common/SupportTicket';

const App = () => {
  const { token } = useContext(AuthContext);

  return (
    <Router>
      <LanguageSelector />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {token ? (
          <>
            <Route path="/customer/create-order" element={<CreateOrder />} />
            <Route path="/customer/order-status" element={<OrderStatus />} />
            <Route path="/customer/order-history" element={<OrderHistory />} />
            <Route path="/customer/chat/:orderId" element={<CustomerChat />} />
            <Route path="/courier/available-orders" element={<AvailableOrders />} />
            <Route path="/courier/active-orders" element={<ActiveOrders />} />
            <Route path="/courier/order-history" element={<CourierOrderHistory />} />
            <Route path="/courier/location-update" element={<LocationUpdate />} />
            <Route path="/courier/chat/:orderId" element={<CourierChat />} />
            <Route path="/admin/dashboard" element={<Dashboard />} />
            <Route path="/admin/alerts" element={<Alerts />} />
            <Route path="/admin/manage-orders" element={<ManageOrders />} />
            <Route path="/admin/geo-view" element={<GeoView />} />
            <Route path="/support/ticket" element={<SupportTicket />} />
          </>
        ) : (
          <Route path="*" element={<Navigate to="/login" />} />
        )}
      </Routes>
    </Router>
  );
};

export default App;