import unittest
import torch
from core.neural_engine import NeuralEngine
from modules.self_healing.system_doctor import SystemDoctor


class TestNeuroSystem(unittest.TestCase):

    def setUp(self):
        self.engine = NeuralEngine(device_map="cpu")

    def test_system_initialization(self):
        self.assertIsNotNone(self.engine)

    def test_health_check(self):
        status = SystemDoctor.health_check()
        self.assertIn('gpu_available', status)
        self.assertIn('ram_usage', status)

    def test_quantum_sampling(self):
        data = torch.rand(10)
        sampled = self.engine.quantum_inspired_sampling(data)
        self.assertEqual(sampled.shape, data.shape)

    def test_anomaly_detection(self):
        from modules.anomaly_detector import AnomalyDetector
        detector = AnomalyDetector()
        data = torch.randn(100, 5)
        detector.train(data.numpy())
        anomaly = detector.detect(torch.randn(5) * 10)
        self.assertTrue(anomaly)


if __name__ == '__main__':
    unittest.main()