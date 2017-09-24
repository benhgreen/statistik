# coding=UTF-8
from django.test import TestCase
import statistik.views

class ViewsTest(TestCase):
    def test__generate_chart_difficulty_display_adds_the_star_if_has_reviewed_is_in_dict(self):
        chart_data = [
            { 
                "difficulty": 12,
                "has_reviewed": True
            },
            {
                "difficulty": 511,
                "has_reviewed": False
            }
        ]
        modified_chart_data = statistik.views._generate_chart_difficulty_display(chart_data)

        self.assertEqual(modified_chart_data[0]['difficulty'], '12★')
        self.assertEqual(modified_chart_data[1]['difficulty'], '511☆')

    def test__generate_chart_difficulty_display_converts_value_to_string_if_has_reviewed_is_not_in_dict(self):
        chart_data = [
            {
                "difficulty": 14
            }
        ]
        modified_chart_data = statistik.views._generate_chart_difficulty_display(chart_data)

        self.assertEqual(modified_chart_data[0]['difficulty'], '14☆')

    def test__generate_chart_bpm_display_sets_bpm_to_min_bpm_if_only_min_bpm_value(self):
        chart_data = [
            {
                "bpm_min": 150
            }
        ]
        modified_chart_data = statistik.views._generate_chart_bpm_display(chart_data)

        self.assertEqual(modified_chart_data[0]['bpm'], '150') 

    def test__generate_chart_bpm_display_sets_bpm_to_correct_value_if_min_and_max_exist(self):
        chart_data = [
            {
                "bpm_min": 160,
                "bpm_max": 320
            }
        ]
        modified_chart_data = statistik.views._generate_chart_bpm_display(chart_data)

        self.assertEqual(modified_chart_data[0]['bpm'], '160 - 320')

    def test__generate_chart_bpm_display_sets_bpm_to_min_value_if_both_min_and_max_are_equal(self):
        chart_data = [
            {
                "bpm_min": 573,
                "bpm_max": 573
            }
        ]
        modified_chart_data = statistik.views._generate_chart_bpm_display(chart_data)

        self.assertEqual(modified_chart_data[0]['bpm'], '573')

    def test__generate_chart_bpm_display_sets_bpm_to_default_if_neither_bpm_value_exists(self):
        chart_data = [{}]
        modified_chart_data = statistik.views._generate_chart_bpm_display(chart_data)

        self.assertEqual(modified_chart_data[0]['bpm'], '--')