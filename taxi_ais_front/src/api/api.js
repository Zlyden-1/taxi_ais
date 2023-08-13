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
        return axios.patch(`http://127.0.0.1:8000/api/references/driver/${vehicleId}/`, changes);
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
    getDriverOptions() {
        return axios.get('http://127.0.0.1:8000/api/references/drivers/options/');
    },
}