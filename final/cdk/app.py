#!/usr/bin/env python3
import aws_cdk as cdk
from transcript_correction_stack import TranscriptCorrectionStack  # ご自身のスタック名に合わせてください

app = cdk.App()
TranscriptCorrectionStack(app, "TranscriptCorrectionStack")
app.synth()
