import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/pages/MainPage'
import DriverList from '@/pages/DriverList'
import VehicleList from '@/pages/VehicleList'
import RentReport from '@/pages/RentReport'

const routes = [
    {
        path: '/',
        component: MainPage
    },
    {
        path: '/refernces/drivers',
        component: DriverList
    },
    {
        path: '/refernces/vehicles',
        component: VehicleList
    },
    {
        path: '/accounting/rent',
        component: RentReport
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router