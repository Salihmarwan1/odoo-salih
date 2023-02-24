import requests from 'requests';

const vehicleRegNo = document.getElementById('vehicle_reg_no').value;
const username = 'salih';
const password = '3xV2qYSKmseESqX';
// free test plate = xzz268

const url = `https://www.regcheck.org.uk/api/json.aspx/CheckSweden/${vehicleRegNo.replace(' ', '')}`;

const getVehicleInfo = async () => {
    const response = await requests.get(url, auth=HTTPBasicAuth(username, password));
    if (response.status === 200) {
        const result = await response.json();
        console.log(result);
    }
};

document.getElementById('get_vehicle_info').addEventListener('click', getVehicleInfo);
