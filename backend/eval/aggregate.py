import json
from pathlib import Path

def aggregate_results(results: list[dict]) -> dict:
    total = len(results)
    if total == 0:
        return {}

    extraction_succeeded = [r for r in results if r['extraction_succeeded']]
    comparable = [r for r in results if r['field_results']]

    extraction_success_rate = (len(extraction_succeeded) / total) * 100
    invalid_output_rate = (100 - extraction_success_rate)

    validation_failure_rate = (
        (sum(1 for r in extraction_succeeded if not r['validation_passed']) / len(extraction_succeeded)) * 100
        if extraction_succeeded else None
    )

    avg_processing_time = (sum(
        r['processing_time_seconds'] for r in results if r['processing_time_seconds'] is not None
    ) / total)

    total_field_checks = 0
    correct_field_checks = 0

    for r in comparable:
        for is_correct in r['field_results'].values():
            total_field_checks += 1
            if is_correct:
                correct_field_checks += 1

    field_level_accuracy = (
        correct_field_checks / total_field_checks if total_field_checks > 0 else None
    ) * 100

    exact_matches = sum(
        1 for r in comparable if all(r['field_results'].values())
    )

    exact_match_accuracy = (exact_matches / len(comparable) if comparable else None) * 100

    error_rate = (sum(
        1 for r in results if r['error']
    ) / total) * 100

    return {
        'total_documents': total,
        'extraction_success_rate': f"{round(extraction_success_rate, 2)}%",
        "invalid_output_rate": f"{round(invalid_output_rate, 2)}%",
        "validation_failure_rate": f"{round(validation_failure_rate, 2) if validation_failure_rate is not None else None}%",
        "average_processing_time_seconds": f"{round(avg_processing_time, 2)} sec",
        "field_level_accuracy": f"{round(field_level_accuracy, 2) if field_level_accuracy is not None else None}%",
        "exact_match_accuracy": f"{round(exact_match_accuracy,2) if exact_match_accuracy is not None else None}%",
        'error_rate_overall': f"{round(error_rate, 2)}%",
        "documents_with_field_comparison": len(comparable),
    }

if __name__ == "__main__":
    results = json.loads(Path('eval/results_po.json').read_text())
    metrics = aggregate_results(results)

    print('\n=== Evaluation Report ===')
    for key, value in metrics.items():
        label = " ".join(word.capitalize() for word in key.split("_"))
        print(f"{label}: {value}")

    Path('eval/aggreagate_po.json').write_text(json.dumps(metrics, indent=2))