#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Performance Benchmark Suite for Radix-Hash Algorithm
Compares Radix-Hash with SHA-256, SHA-3, and other standard algorithms
"""

import time
import hashlib
import psutil
import os
import tracemalloc
import statistics
from typing import List, Dict, Any
import sys

# Import your Radix-Hash implementation
# Adjust the import path according to your project structure
try:
    from model.radix_hash import process_block
    RADIX_HASH_AVAILABLE = True
except ImportError:
    print("Warning: Radix-Hash module not found. Please adjust import path.")
    RADIX_HASH_AVAILABLE = False
    
    # Dummy function for testing
    def process_block(text: str) -> str:
        return "0" * 772

class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
        self.test_data = self._generate_test_data()
    
    def _generate_test_data(self) -> Dict[str, List[str]]:
        """Generate various test datasets"""
        return {
            "small": [
                "hello",
                "test",
                "a",
                "123",
                "Hello World!"
            ],
            "medium": [
                "This is a medium length test string for performance evaluation." * 10,
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit." * 20,
                "Performance testing with various input sizes and patterns." * 15,
                "A" * 1000,
                "0123456789" * 100
            ],
            "large": [
                "Large text data for comprehensive performance analysis." * 1000,
                "X" * 10000,
                "The quick brown fox jumps over the lazy dog." * 2000,
                "Lorem ipsum " * 5000,
                "Performance benchmark data " * 3000
            ],
            "patterns": [
                "a" * 10000,  # Repeated character
                "ab" * 5000,  # Simple pattern
                "0123456789" * 1000,  # Numeric pattern
                "AbCdEfGhIjKlMnOpQrStUvWxYz" * 400,  # Mixed case
                "\x00\x01\x02\x03" * 2500  # Binary pattern
            ]
        }
    
    def measure_time_and_memory(self, func, data: str) -> Dict[str, Any]:
        """Measure execution time and memory usage for a function"""
        # Memory measurement
        tracemalloc.start()
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        
        # Time measurement
        start_time = time.perf_counter()
        result = func(data)
        end_time = time.perf_counter()
        
        # Memory after
        memory_after = process.memory_info().rss
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return {
            'result': result,
            'time': end_time - start_time,
            'memory_peak': peak,
            'memory_diff': memory_after - memory_before,
            'input_size': len(data)
        }
    
    def radix_hash_wrapper(self, text: str) -> str:
        """Wrapper for Radix-Hash"""
        return process_block(text)
    
    def sha256_wrapper(self, text: str) -> str:
        """Wrapper for SHA-256"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def sha3_256_wrapper(self, text: str) -> str:
        """Wrapper for SHA3-256"""
        return hashlib.sha3_256(text.encode('utf-8')).hexdigest()
    
    def sha3_512_wrapper(self, text: str) -> str:
        """Wrapper for SHA3-512"""
        return hashlib.sha3_512(text.encode('utf-8')).hexdigest()
    
    def blake2b_wrapper(self, text: str) -> str:
        """Wrapper for BLAKE2b"""
        return hashlib.blake2b(text.encode('utf-8')).hexdigest()
    
    def run_algorithm_benchmark(self, algorithm_name: str, func, test_category: str) -> Dict:
        """Run benchmark for a specific algorithm on a test category"""
        results = []
        
        for test_data in self.test_data[test_category]:
            try:
                measurement = self.measure_time_and_memory(func, test_data)
                results.append(measurement)
            except Exception as e:
                print(f"Error testing {algorithm_name} on {test_category}: {e}")
                continue
        
        if not results:
            return {}
        
        # Calculate statistics
        times = [r['time'] for r in results]
        memories = [r['memory_peak'] for r in results]
        input_sizes = [r['input_size'] for r in results]
        
        return {
            'algorithm': algorithm_name,
            'category': test_category,
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'median_time': statistics.median(times),
            'avg_memory': statistics.mean(memories),
            'max_memory': max(memories),
            'avg_input_size': statistics.mean(input_sizes),
            'throughput_mb_s': statistics.mean([size/time/1024/1024 for size, time in zip(input_sizes, times) if time > 0]),
            'samples': len(results)
        }
    
    def run_full_benchmark(self) -> Dict:
        """Run comprehensive benchmark on all algorithms and test categories"""
        algorithms = {
            'Radix-Hash': self.radix_hash_wrapper,
            'SHA-256': self.sha256_wrapper,
            'SHA3-256': self.sha3_256_wrapper,
            'SHA3-512': self.sha3_512_wrapper,
            'BLAKE2b': self.blake2b_wrapper
        }
        
        if not RADIX_HASH_AVAILABLE:
            print("Warning: Running benchmark with dummy Radix-Hash implementation")
        
        results = {}
        
        for alg_name, alg_func in algorithms.items():
            results[alg_name] = {}
            print(f"\nTesting {alg_name}...")
            
            for category in self.test_data.keys():
                print(f"  - {category} inputs...")
                category_result = self.run_algorithm_benchmark(alg_name, alg_func, category)
                if category_result:
                    results[alg_name][category] = category_result
        
        return results
    
    def generate_performance_report(self, results: Dict) -> str:
        """Generate a comprehensive performance report"""
        report = ["=" * 80]
        report.append("RADIX-HASH PERFORMANCE BENCHMARK REPORT")
        report.append("=" * 80)
        report.append("")
        
        # System info
        report.append("System Information:")
        report.append(f"- CPU: {psutil.cpu_count()} cores")
        report.append(f"- Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
        report.append(f"- Python: {sys.version}")
        report.append("")
        
        # Performance comparison table
        report.append("PERFORMANCE COMPARISON (Average Values)")
        report.append("-" * 80)
        report.append(f"{'Algorithm':<15} {'Category':<10} {'Time (ms)':<12} {'Memory (KB)':<12} {'Throughput (MB/s)':<15}")
        report.append("-" * 80)
        
        for alg_name in results:
            for category in results[alg_name]:
                data = results[alg_name][category]
                report.append(f"{alg_name:<15} {category:<10} "
                            f"{data['avg_time']*1000:<12.3f} "
                            f"{data['avg_memory']/1024:<12.1f} "
                            f"{data.get('throughput_mb_s', 0):<15.2f}")
        
        report.append("")
        
        # Detailed analysis for each algorithm
        for alg_name in results:
            report.append(f"\n{alg_name} - DETAILED ANALYSIS")
            report.append("-" * 40)
            
            for category in results[alg_name]:
                data = results[alg_name][category]
                report.append(f"\n{category.upper()} INPUTS:")
                report.append(f"  Average time: {data['avg_time']*1000:.3f} ms")
                report.append(f"  Min time: {data['min_time']*1000:.3f} ms")
                report.append(f"  Max time: {data['max_time']*1000:.3f} ms")
                report.append(f"  Median time: {data['median_time']*1000:.3f} ms")
                report.append(f"  Average memory: {data['avg_memory']/1024:.1f} KB")
                report.append(f"  Max memory: {data['max_memory']/1024:.1f} KB")
                report.append(f"  Throughput: {data.get('throughput_mb_s', 0):.2f} MB/s")
                report.append(f"  Samples: {data['samples']}")
        
        # Relative performance analysis
        if 'Radix-Hash' in results and 'SHA-256' in results:
            report.append("\n" + "=" * 50)
            report.append("RADIX-HASH vs SHA-256 COMPARISON")
            report.append("=" * 50)
            
            for category in results['Radix-Hash']:
                if category in results['SHA-256']:
                    radix_time = results['Radix-Hash'][category]['avg_time']
                    sha256_time = results['SHA-256'][category]['avg_time']
                    speed_ratio = sha256_time / radix_time if radix_time > 0 else 0
                    
                    radix_memory = results['Radix-Hash'][category]['avg_memory']
                    sha256_memory = results['SHA-256'][category]['avg_memory']
                    memory_ratio = radix_memory / sha256_memory if sha256_memory > 0 else 0
                    
                    report.append(f"\n{category.upper()} Category:")
                    if speed_ratio > 1:
                        report.append(f"  Radix-Hash is {speed_ratio:.2f}x FASTER than SHA-256")
                    else:
                        report.append(f"  SHA-256 is {1/speed_ratio:.2f}x faster than Radix-Hash")
                    
                    if memory_ratio > 1:
                        report.append(f"  Radix-Hash uses {memory_ratio:.2f}x MORE memory than SHA-256")
                    else:
                        report.append(f"  Radix-Hash uses {1/memory_ratio:.2f}x LESS memory than SHA-256")
        
        return "\n".join(report)
    
    def save_results(self, results: Dict, report: str, filename_prefix: str = "radix_hash_benchmark"):
        """Save benchmark results to files"""
        import json
        
        # Save raw results as JSON
        with open(f"{filename_prefix}_results.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save report as text
        with open(f"{filename_prefix}_report.txt", 'w') as f:
            f.write(report)
        
        print(f"\nResults saved:")
        print(f"- {filename_prefix}_results.json")
        print(f"- {filename_prefix}_report.txt")

def main():
    """Main benchmark execution"""
    print("Starting Radix-Hash Performance Benchmark...")
    print("This may take several minutes to complete.\n")
    
    benchmark = PerformanceBenchmark()
    results = benchmark.run_full_benchmark()
    
    print("\nGenerating report...")
    report = benchmark.generate_performance_report(results)
    
    print(report)
    
    # Save results
    benchmark.save_results(results, report)
    
    print("\nBenchmark completed!")

if __name__ == "__main__":
    main()