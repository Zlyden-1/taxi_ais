import axios from "axios";

export default {
    getDrivers() {
        return axios.get('http://127.0.0.1:8000/api/references/drivers/');
    },
    createDriver(driverData) {
        return axios.post('http://127.0.0.1:8000/api/references/drivers/create/', driverData);
    },
    deleteDriver(driverId) {
        return axios.delete(`http://127.0.0.1:8000/api/references/driver/${driverId}/`);
    },
    getDriver(driverId) {
        return axios.get(`http://127.0.0.1:8000/api/references/driver/${driverId}/`);
    },
    patchDriver(driverId, changes) {
        return axios.patch(`http://127.0.0.1:8000/api/references/driver/${driverId}/`, changes);
    },
    getVehicle(vehicleId) {
        return axios.get(`http://127.0.0.1:8000/api/references/vehicle/${vehicleId}/`);
    },
    getVehicles() {
        return axios.get(`http://127.0.0.1:8000/api/references/vehicles/`);
    },
    createVehicle(vehicleData) {
        return axios.post('http://127.0.0.1:8000/api/references/vehicles/create/', vehicleData);
    },
    patchVehicle(vehicleId, changes) {
        return axios.patch(`http://127.0.0.1:8000/api/references/vehicle/${vehicleId}/`, changes);
    },
    deleteVehicle(vehicleId) {
        return axios.delete(`http://127.0.0.1:8000/api/references/vehicle/${vehicleId}/`);
    },
    getVehicleTypeOptions() {
        return axios.get('http://127.0.0.1:8000/api/references/vehicles/types/');
    },
    getVehicleStatusOptions() {
        return axios.get('http://127.0.0.1:8000/api/references/vehicles/statuses/');
    },
    getVehicleLocationOptions() {
        return axios.get('http://127.0.0.1:8000/api/references/vehicles/locations/');
    },
    getDriverOptionsForVehicles() {
        return axios.get('http://127.0.0.1:8000/api/references/drivers/options/for_vehicles/');
    },
    getDriverOptionsForRents() {
        return axios.get('http://127.0.0.1:8000/api/references/drivers/options/for_rents/');
    },
    getVehicleHistory(vehicleId) {
        return axios.get(`http://127.0.0.1:8000/api/references/vehicle/${vehicleId}/usage_history/`)
    },
    getRents(startDate, endDate) {
        return axios.get(`http://127.0.0.1:8000/api/accounting/rents/`, {
            params: {
                start_date: startDate,
                end_date: endDate,
            }
        })
    }
}