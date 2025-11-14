"""
Performance Testing Framework for Carmichael Number Database Implementations

This package provides tools for comparing query performance between different
database storage strategies for Carmichael numbers.
"""

from .database_interface import CarmichaelDatabase, SingleTableDB, MultiTableDB
from .test_case_loader import TestCase, TestCaseLoader
from .test_runner import TestRunner, TestRunStats, QueryResult
from .visualizer import PerformanceVisualizer

__version__ = "1.0.0"
__all__ = [
    "CarmichaelDatabase",
    "SingleTableDB",
    "MultiTableDB",
    "TestCase",
    "TestCaseLoader",
    "TestRunner",
    "TestRunStats",
    "QueryResult",
    "PerformanceVisualizer",
]
