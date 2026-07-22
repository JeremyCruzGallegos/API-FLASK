import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:5000';

export const successfulRequests = new Counter('successful_requests');
export const failedRequests = new Counter('failed_requests');
export const errorRate = new Rate('error_rate');

export const options = {
  scenarios: {
    usuarios_20: {
      executor: 'constant-vus',
      vus: 20,
      duration: '30s',
      exec: 'inventoryScenario',
      tags: { scenario_name: '20 usuarios - 30 segundos' },
    },
    usuarios_50: {
      executor: 'constant-vus',
      vus: 50,
      duration: '45s',
      startTime: '35s',
      exec: 'inventoryScenario',
      tags: { scenario_name: '50 usuarios - 45 segundos' },
    },
    usuarios_100: {
      executor: 'constant-vus',
      vus: 100,
      duration: '60s',
      startTime: '85s',
      exec: 'inventoryScenario',
      tags: { scenario_name: '100 usuarios - 60 segundos' },
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
  },
};

export function inventoryScenario() {
  const productPayload = JSON.stringify({
    nombre: `Producto k6 ${__VU}-${__ITER}`,
    precio: 120.5,
    cantidad: 8,
  });

  const params = { headers: { 'Content-Type': 'application/json' } };

  record(http.get(`${BASE_URL}/productos`), 200, 'listar productos');
  const createResponse = http.post(`${BASE_URL}/productos`, productPayload, params);
  record(createResponse, 201, 'crear producto');

  if (createResponse.status === 201) {
    const productId = createResponse.json('id');
    record(http.get(`${BASE_URL}/productos/${productId}`), 200, 'obtener producto');
    record(
      http.put(
        `${BASE_URL}/productos/${productId}`,
        JSON.stringify({ nombre: `Producto actualizado ${productId}`, precio: 150, cantidad: 12 }),
        params,
      ),
      200,
      'actualizar producto',
    );
    record(http.del(`${BASE_URL}/productos/${productId}`), 204, 'eliminar producto');
  }

  sleep(1);
}

function record(response, expectedStatus, name) {
  const ok = check(response, {
    [`${name} responde ${expectedStatus}`]: (res) => res.status === expectedStatus,
  });

  if (ok) {
    successfulRequests.add(1);
    errorRate.add(false);
  } else {
    failedRequests.add(1);
    errorRate.add(true);
  }
}
