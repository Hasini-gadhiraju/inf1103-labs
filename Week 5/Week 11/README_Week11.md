# INF1103 Lab 9 — Week 11 submission

This project builds on the supplied Week 10 / Lab 8 project. Existing JSON inventory, supplier, physical/digital properties, order lines and tests remain included.

## Run

```bash
python -m unittest discover -v
python demo_lab9.py
python inventory_manager.py
```

Run the CSV demonstration from the project directory. The main menu includes option 10 to change a saved in-memory order's discount.

## Docker example (run locally)

```bash
docker build -t inf1103-week11 .
docker run --rm inf1103-week11
# Automated tests in a container:
docker run --rm inf1103-week11 python -m unittest discover -v
# Demo in a container:
docker run --rm inf1103-week11 python demo_lab9.py
```

## Git example (run in your OWN repo)

```bash
git status
git add .
git commit -m "Implement Week 11 strategy, factory, validation and tests"
git push
git log -5 --oneline
```

## Week 11 changes

- `discount_strategy.py`: abstract strategy, no discount, percentage, bulk, and student 5%.
- `order.py`: injectable default discount, `set_discount()`, delegated total calculation.
- `product_factory.py`: product creation with preserved weight/download-size fields.
- `product.py`, `order_line.py`: price, stock and quantity validation.
- `input_helpers.py`: retrying positive-price input.
- `csv_loader.py`, `products.csv`: CSV loading and resilient per-row errors.
- `tests/test_lab9.py`: new automated tests, alongside updated Week 10 tests.
- `UML_Week11.png` / `.dot`: updated class diagram.
- `Predict_First_Week11.docx`: predictions, observed results, and changes/reflections.

**Still needed from you:** capture genuine new screenshots of `git status`, `git log`, Docker build/run and Docker test runs after executing the commands on your own machine. The Week 10 screenshots in `Week10_Reference/` are historical evidence only, NOT Week 11 workflow evidence. Review your own prediction notes before submitting; the document contains suggested model answers and verified outcomes.
